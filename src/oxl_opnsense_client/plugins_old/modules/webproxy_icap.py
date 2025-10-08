from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.webproxy_icap import General


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        request_url=dict(
            type='str', required=False, default='icap://[::1]:1344/avscan',
            aliases=['request', 'request_target'],
            description='The url where the REQMOD requests should be sent to'
        ),
        response_url=dict(
            type='str', required=False, default='icap://[::1]:1344/avscan',
            aliases=['response', 'response_target'],
            description='The url where the RESPMOD requests should be sent to'
        ),
        ttl=dict(
            type='int', required=False, default=60, aliases=['default_ttl']
        ),
        send_client_ip=dict(
            type='bool', required=False, default=True, aliases=['send_client'],
            description='If you enable this option, the client IP address will be sent to '
                        'the ICAP server. This can be useful if you want to filter traffic '
                        'based on IP addresses'
        ),
        send_username=dict(
            type='bool', required=False, default=False, aliases=['send_user'],
            description='If you enable this option, the username of the client will be sent '
                        'to the ICAP server. This can be useful if you want to filter traffic '
                        'based on usernames. Authentication is required to use usernames'
        ),
        encode_username=dict(
            type='bool', required=False, default=False,
            aliases=['user_encode', 'encode_user', 'enc_user'],
            description='Use this option if your usernames need to be encoded'
        ),
        header_username=dict(
            type='str', required=False, default='X-Username',
            aliases=['header_user', 'user_header'],
            description='The header which should be used to send the username to the ICAP server'
        ),
        preview=dict(
            type='bool', required=False, default=True,
            description='If you use previews, only a part of the data is sent '
                        'to the ICAP server. Setting this option can improve the performance'
        ),
        preview_size=dict(
            type='int', required=False, default=1024,
            description='Size of the preview which is sent to the ICAP server'
        ),
        exclude=dict(
            type='list', elements='str', required=False, default=[],
            description='Exclusion list destination domains.You may use a regular expression, '
                        'use a comma or press Enter for new item. Examples: "mydomain.com" matches '
                        'on "*.mydomain.com"; "https://([a-zA-Z]+)\\.mydomain\\." matches on '
                        '"http(s)://textONLY.mydomain.*"; "\\.gif$" matches on "\\*.gif" but not on '
                        '"\\*.gif\\test"; "\\[0-9]+\\.gif$" matches on "\\123.gif" but not on "\\test.gif"'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(General(m=module_input, result=result))
    return result
