from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import RELOAD_MOD_ARG_DEF_FALSE, STATE_ONLY_MOD_ARG
from ..module_utils.main.ipsec_cert import KeyPair


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(type='str', required=True),
        public_key=dict(type='str', required=False, aliases=['pub_key', 'pub']),
        private_key=dict(type='str', required=False, aliases=['priv_key', 'priv'], no_log=True),
        type=dict(type='str', required=False, choices=['rsa'], default='rsa'),
        **RELOAD_MOD_ARG_DEF_FALSE,
        **STATE_ONLY_MOD_ARG,
    )


    validate_input(i=module_input, definition=module_args)
    module_wrapper(KeyPair(m=module_input, result=result))
    return result
