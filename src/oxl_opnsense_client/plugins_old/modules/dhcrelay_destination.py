from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.dhcrelay_destination import DhcRelayDestination


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(
            type='str', required=True,
            description='A unique name for this relay destination.',
        ),
        server=dict(
            type='list', elements='str', required=False,
            description='A list of server IP addresses to relay DHCP requests to.'
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(DhcRelayDestination(m=module_input, result=result))
    return result
