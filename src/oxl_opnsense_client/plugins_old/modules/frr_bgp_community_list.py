from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_bgp_community_list import Community


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        description=dict(type='str', required=True, aliases=['desc']),
        number=dict(type='str', required=False, aliases=['nr']),
        seq=dict(type='int', required=False, aliases=['seq_number']),
        action=dict(type='str', required=False, options=['permit', 'deny']),
        community=dict(
            type='str', required=False, aliases=['comm'],
            description='The community you want to match. You can also regex and it is '
                        'not validated so please be careful.'
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Community(m=module_input, result=result))
    return result
