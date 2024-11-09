from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.interface_vlan import Vlan


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        device=dict(
            type='str', required=False, aliases=['vlanif'],
            description="Optional 'device' of the entry. Needs to start with 'vlan0'",
        ),
        interface=dict(
            type='str', required=False, aliases=['parent', 'port', 'int', 'if'],
            description='Existing VLAN capable interface - you must provide the network '
                        "port as shown in 'Interfaces - Assignments - Network port'"
        ),
        vlan=dict(
            type='int', required=False, aliases=['tag', 'id'],
            description='802.1Q VLAN tag (between 1 and 4094)'
        ),
        priority=dict(
            type='int', required=False, default=0, aliases=['prio', 'pcp'],
            description='802.1Q VLAN PCP (priority code point)'
        ),
        description=dict(type='str', required=True, aliases=['desc', 'name']),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Vlan(m=module_input, result=result))
    return result
