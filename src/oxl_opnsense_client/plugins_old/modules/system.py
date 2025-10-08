from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.system import wait_for_response, get_upgrade_status, wait_for_update


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = {
        **valid_results(result),
        **{
            'changed': True,
            'failed': False,
            'timeout_exceeded': False,
        }
    }

    module_args = dict(
        action=dict(
            type='str', required=True,
            choices=['poweroff', 'reboot', 'update', 'upgrade', 'audit'],
            description="WARNING: Only use the 'upgrade' option in test-environments. "
                        "In production you should use the WebUI to upgrade!"
        ),
        wait=dict(type='bool', required=False, default=True),
        wait_timeout=dict(type='int', required=False, default=90),
        poll_interval=dict(type='int', required=False, default=2),
        force_upgrade=dict(type='bool', required=False, default=False),
    )

    validate_input(i=module_input, definition=module_args)

    if m.params['action'] == 'upgrade' and not m.params['force_upgrade']:
        m.fail(
            "If you really want to perform an upgrade - you need to additionally supply the 'force_upgrade' argument. "
            "WARNING: Using the 'upgrade' action is only recommended for test-environments. "
            "In production you should use the WebUI to upgrade!"
        )

    if not m.check_mode:
        upgrade_status = get_upgrade_status(m.c.session)
        if upgrade_status['status'] not in ['done', 'error']:
            m.fail(
                f'System may be upgrading! System-actions are currently blocked! Details: {upgrade_status}'
            )

        m.c.session.post({
            'command': m.params['action'],
            'module': 'core',
            'controller': 'firmware',
        })

        if m.params['wait']:
            if m.params['debug']:
                m.warn(f"Waiting for firewall to complete '{m.params['action']}'!")

            try:
                if m.params['action'] in ['upgrade', 'update']:
                    result['failed'] = not wait_for_update(m=m, s=m.c.session)

                elif m.params['action'] == 'reboot':
                    result['failed'] = not wait_for_response(m=m)

            except TimeoutError:
                result['timeout_exceeded'] = True

    return result
