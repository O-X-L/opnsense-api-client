from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.webproxy_remote_acl import Acl


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        file=dict(
            type='str', required=True, aliases=['filename'],
            description='Unique file-name to store the remote acl in'
        ),
        url=dict(
            type='str', required=False,
            description='Url to fetch the acl from'
        ),
        username=dict(
            type='str', required=False, aliases=['user'],
            description='Optional user for authentication'
        ),
        password=dict(
            type='str', required=False, aliases=['pwd'],
            description='Optional password for authentication',
            no_log=True,
        ),
        categories=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['cat', 'filter'],
            description='Select categories to use, leave empty for all. '
                        'Categories are visible in the WEB-UI after initial download'
        ),
        verify_ssl=dict(
            type='bool', required=False, default=True, aliases=['verify'],
            description='If certificate validation should be done - relevant if '
                        'self-signed certificates are used on the target server!'
        ),
        description=dict(
            type='str', required=False, aliases=['desc'],
            description='A description to explain what this blacklist is intended for'
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Acl(m=module_input, result=result))
    return result
