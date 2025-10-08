from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.webproxy_general import General


BLANK_VALUES = {
    'errors': 'squid',
    'log_target': 'file',
    'handling_forwarded_for': 'default',
}


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        errors=dict(
            type='str', required=False, default='opnsense', aliases=['error_pages'],
            choices=['opnsense', 'custom', 'squid'],
            description='The proxy error pages can be altered, default layout uses '
                        'OPNsense content, when Squid is selected the content for the '
                        'selected language will be used (standard squid layout), Custom '
                        'offers the possibility to upload your own theme content'
        ),
        icp_port=dict(type='int', required=False, aliases=['icp']),
        log=dict(type='bool', required=False, default=True),
        log_store=dict(type='bool', required=False, default=True),
        log_target=dict(
            type='str', required=False, default='file',
            choices=['file', 'file_extendend', 'file_json', 'syslog', 'syslog_json'],
            description='Send log data to the selected target. When syslog is selected, '
                        'facility local 4 will be used to send messages of info level for these logs'
        ),
        log_ignore=dict(
            type='list', elements='str', required=False, default=[],
            description='Type subnets/addresses you want to ignore for the access.log'
        ),
        dns_servers=dict(
            type='list', elements='str', required=False, default=[],
            description='IPs of alternative DNS servers you like to use'
        ),
        use_via_header=dict(
            type='bool', required=False, default=True,
            description='If set (default), Squid will include a Via header in requests and replies '
                        'as required by RFC2616'
        ),
        handling_forwarded_for=dict(
            type='str', required=False, default='default',
            aliases=['forwarded_for_handling', 'forwarded_for', 'handle_ff'],
            choices=['default', 'on', 'off', 'transparent', 'delete', 'truncate'],
            description="Select what to do with X-Forwarded-For header. If set to: 'on', Squid will "
                        "append your client's IP address in the HTTP requests it forwards. By default "
                        "it looks like X-Forwarded-For: 192.1.2.3; If set to: 'off', it will appear as "
                        "X-Forwarded-For: unknown; 'transparent', Squid will not alter the X-Forwarded-For "
                        "header in any way; If set to: 'delete', Squid will delete the entire "
                        "X-Forwarded-For header; If set to: 'truncate', Squid will remove all existing "
                        "X-Forwarded-For entries, and place the client IP as the sole entry"
        ),
        hostname=dict(
            type='str', required=False, aliases=['visible_hostname'],
            description='The hostname to be displayed in proxy server error messages'
        ),
        email=dict(
            type='str', required=False, default='admin@localhost.local', aliases=['visible_email'],
            description='The email address displayed in error messages to the users'
        ),
        suppress_version=dict(
            type='bool', required=False, default=False,
            description='Suppress Squid version string info in HTTP headers and HTML error pages'
        ),
        connect_timeout=dict(
            type='int', required=False,
            description='This can help you when having connection issues with IPv6 enabled servers. '
                        'Set a value in seconds (1-120s)'
        ),
        handling_uri_whitespace=dict(
            type='str', required=False, default='strip',
            aliases=['uri_whitespace_handling', 'uri_whitespace', 'handle_uw'],
            choices=['strip', 'deny', 'allow', 'encode', 'chop'],
            description='Select what to do with URI that contain whitespaces. The current Squid '
                        'implementation of encode and chop violates RFC2616 by not using a 301 '
                        'redirect after altering the URL'
        ),
        pinger=dict(
            type='bool', required=False, default=True,
            description='Toggles the Squid pinger service. '
                        'This service is used in the selection of the best parent proxy'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(General(m=module_input, result=result))
    return result
