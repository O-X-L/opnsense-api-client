from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_ospf_prefix_list import Prefix


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(type='str', required=True),
        seq=dict(type='int', required=False, aliases=['seq_number']),
        action=dict(type='str', required=False, options=['permit', 'deny']),
        network=dict(type='str', required=False, aliases=['net']),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Prefix(m=module_input, result=result))
    return result
