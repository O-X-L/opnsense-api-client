from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import RELOAD_MOD_ARG_DEF_FALSE, STATE_ONLY_MOD_ARG
from ..module_utils.main.ipsec_psk import PreSharedKey


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        identity_local=dict(
            type='str', required=True, aliases=['identity', 'ident'],
            description='This can be either an IP address, fully qualified domain name or an email address.'
        ),
        identity_remote=dict(
            type='str', required=False, aliases=['remote_ident'],
            description='(optional) This can be either an IP address, fully qualified domain name or '
                        'an email address to identify the remote host.'
        ),
        psk=dict(type='str', required=False, no_log=True, aliases=['key', 'secret']),
        type=dict(
            type='str', required=False, choices=['PSK', 'EAP'], default='PSK', aliases=['kind'],
        ),
        **RELOAD_MOD_ARG_DEF_FALSE,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(PreSharedKey(m=module_input, result=result))
    return result
