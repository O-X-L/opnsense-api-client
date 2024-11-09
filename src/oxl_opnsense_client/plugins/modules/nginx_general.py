from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.nginx_general import General


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        ban_ttl=dict(type='int', required=False, default=0),
        **EN_ONLY_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(General(m=module_input, result=result))
    return result
