from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import RELOAD_MOD_ARG_DEF_FALSE
from ..module_utils.defaults.alias import ALIAS_MOD_ARGS
from ..module_utils.main.alias import Alias


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        **RELOAD_MOD_ARG_DEF_FALSE,  # default-true takes pretty long sometimes (urltables and so on)
        **ALIAS_MOD_ARGS
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Alias(m=module_input, result=result))
    return result
