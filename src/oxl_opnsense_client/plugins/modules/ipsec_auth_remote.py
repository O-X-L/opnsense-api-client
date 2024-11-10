from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.defaults.ipsec_auth import IPSEC_AUTH_MOD_ARGS
from ..module_utils.main.ipsec_auth_remote import Auth


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        **IPSEC_AUTH_MOD_ARGS,
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Auth(m=module_input, result=result))
    return result
