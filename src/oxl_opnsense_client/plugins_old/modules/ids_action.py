from ..module_input import validate_input, ModuleInput, valid_results


ACTION_MAPPING = {
    'get_alert_info': {'a': 'getAlertInfo', 'post': False},
    'get_alert_logs': {'a': 'getAlertLogs', 'post': False},
    'query_alerts': {'a': 'queryAlerts', 'post': False},
    'status': {'post': False},
    'reconfigure': {'post': True},
    'restart': {'post': True},
    'start': {'post': True},
    'stop': {'post': True},
    'drop_alert_log': {'a': 'dropAlertLog', 'post': True},
    'reload_rules': {'a': 'reloadRules', 'post': True},
    'update_rules': {'a': 'updateRules', 'post': True},
}


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    module_args = dict(
        action=dict(
            type='str', required=True, aliases=['do', 'a'],
            choices=[
                'get_alert_logs', 'query_alerts', 'get_alert_info', 'status',
                'reconfigure', 'restart', 'start', 'stop',
                'drop_alert_log', 'reload_rules', 'update_rules',
            ],
        ),
        alert_id=dict(
            type='str', required=False, aliases=['alert'],
            description="Parameter Alert-ID needed for 'get_alert_info'",
        ),
    )

    validate_input(i=module_input, definition=module_args)

    action = m.params['action']
    if action == 'get_alert_info' and m.params['alert_id'] is None:
        m.fail("You need to provide an Alert-ID as 'alert_id' to execute 'get_alert_info'!")

    # translate actions to api-commands
    cmd = action
    if 'a' in ACTION_MAPPING[action]:
        cmd = ACTION_MAPPING[action]['a']

    result['executed'] = cmd

    # execute action or pull status
    if ACTION_MAPPING[action]['post']:
        result['changed'] = True

        if not m.check_mode:
            m.c.session.get(
                cnf={
                    'module': 'ids',
                    'controller': 'service',
                    'command': cmd,
                }
            )

    else:
        params = []
        if m.params['alert_id'] is not None:
            params = [m.params['alert_id']]

        info = m.c.session.get(
            cnf={
                'module': 'ids',
                'controller': 'service',
                'command': cmd,
                'params': params,
            }
        )

        if 'response' in info:
            info = info['response']

            if isinstance(info, str):
                info = info.strip()

        result['data'] = info

    return result
