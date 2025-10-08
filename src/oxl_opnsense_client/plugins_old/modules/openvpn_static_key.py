from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.openvpn_static_key import Key


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['desc', 'description'],
            description='The name used to match this config to existing entries'
        ),
        mode=dict(
            type='str', required=False, default='crypt', aliases=['type'], choices=['auth', 'crypt'],
            description='Define the use of this key, authentication (--tls-auth) or authentication and '
                        'encryption (--tls-crypt)'
        ),
        key=dict(
            type='str', required=False, no_log=True,
            description='OpenVPN Static key. If empty - it will be auto-generated.'
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Key(m=module_input, result=result))
    return result
