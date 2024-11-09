from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.unbound_acl import Acl


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['n'],
            decription='Provide an access list name',
        ),
        action=dict(
            type='str', required=False, default='allow',
            choices=['allow', 'deny', 'refuse', 'allow_snoop', 'deny_non_local', 'refuse_non_local'],
            decription='Choose what to do with DNS requests that match the criteria specified below: '
                       '* DENY: This action stops queries from hosts within the netblock defined below. '
                       '* REFUSE: This action also stops queries from hosts within the netblock defined below, '
                       'but sends a DNS rcode REFUSED error message back to the client. '
                       '* ALLOW: This action allows queries from hosts within the netblock defined below. '
                       '* ALLOW SNOOP: This action allows recursive and nonrecursive access from hosts within '
                       'the netblock defined below. '
                       'Used for cache snooping and ideally should only be configured for your administrative host. '
                       '* DENY NON-LOCAL: Allow only authoritative local-data queries from hosts within the netblock '
                       'defined below. Messages that are disallowed are dropped. '
                       '* REFUSE NON-LOCAL: Allow only authoritative local-data queries from hosts within the '
                       'netblock defined below. '
                       'Sends a DNS rcode REFUSED error message back to the client for messages that are disallowed.',
        ),
        networks=dict(
            type='list', elements='str', required=False, aliases=['nets'],
            decription='List of networks in CIDR notation to apply this ACL on. For example: 192.168.1.0/24',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Acl(m=module_input, result=result))
    return result
