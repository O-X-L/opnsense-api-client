from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.dhcrelay_relay import DhcRelayRelay


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        enabled=dict(
            type='bool', default=False,
            description='Enable or disable this relay.',
        ),
        interface=dict(
            type='str', required=True, aliases=['i', 'int'],
            description='The interface to relay DHCP requests from. '
        ),
        destination=dict(
            type='str', required=False, aliases=['dest'],
            description='The uuid of the destination server group to relay DHCP requests to.'
        ),
        agent_info=dict(
            type='bool', default=False,
            description='Add the relay agent information option.',
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(DhcRelayRelay(m=module_input, result=result))

    return result
