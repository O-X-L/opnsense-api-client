from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_ospf_general import General


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        carp=dict(
            type='bool', required=False, default=False, aliases=['carp_demote'],
            description='Register CARP status monitor, when no neighbors are found, '
                        'consider this node less attractive. This feature needs syslog '
                        'enabled using "Debugging" logging to catch all relevant status '
                        'events. This option is not compatible with "Enable CARP Failover"'
        ),
        id=dict(
            type='str', required=False, aliases=['router_id'],
            description='If you have a CARP setup, you may want to configure a router id '
                        'in case of a conflict'
        ),
        redistribute=dict(
            type='list', elements='str', required=False, default=[],
            options=['connected', 'kernel', 'static'],
            description='Select other routing sources, which should be '
                        'redistributed to the other nodes'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(General(m=module_input, result=result))
    return result
