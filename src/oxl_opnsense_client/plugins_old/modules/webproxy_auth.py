from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import RELOAD_MOD_ARG
from ..module_utils.main.webproxy_auth import General


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        method=dict(
            type='str', required=False, aliases=['type', 'target'],
            description='The authentication backend to use - as shown in the '
                        "WEB-UI at 'System - Access - Servers'. Per example: "
                        "'Local Database'"
        ),
        group=dict(
            type='str', required=False, aliases=['local_group'],
            description='Restrict access to users in the selected (local)group. '
                        "NOTE: please be aware that users (or vouchers) which aren't "
                        "administered locally will be denied when using this option"
        ),
        prompt=dict(
            type='str', required=False, aliases=['realm'],
            default='OPNsense proxy authentication',
            description='The prompt will be displayed in the authentication request window'
        ),
        ttl_h=dict(
            type='int', required=False, default=2, aliases=['ttl', 'ttl_hours', 'credential_ttl'],
            description='This specifies for how long (in hours) the proxy server assumes '
                        'an externally validated username and password combination is valid '
                        '(Time To Live). When the TTL expires, the user will be prompted for '
                        'credentials again'
        ),
        processes=dict(
            type='int', required=False, default=5, aliases=['proc'],
            description='The total number of authenticator processes to spawn'
        ),
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(General(m=module_input, result=result))
    return result
