from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.bind_domain import Domain


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(type='str', required=True, aliases=['domain_name', 'domain']),
        mode=dict(
            type='str', required=False, default='primary', choices=['primary', 'secondary']
        ),
        primary=dict(
            type='list', elements='str', required=False, aliases=['primary_ip', 'master', 'master_ip'], default=[],
            description='Set the IP address of primary server when using secondary mode'
        ),
        transfer_key_algo=dict(
            type='str', required=False,
            choices=[
                'hmac-sha512', 'hmac-sha384', 'hmac-sha256', 'hmac-sha224',
                'hmac-sha1', 'hmac-md5',
            ]
        ),
        transfer_key_name=dict(type='str', required=False),
        transfer_key=dict(type='str', required=False, no_log=True),
        allow_notify=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['allow_notify_secondary', 'allow_notify_slave'],
            description='A list of allowed IP addresses to receive notifies from'
        ),
        transfer_acl=dict(
            type='list', elements='str', required=False, default=[], aliases=['allow_transfer'],
            description='An ACL where you allow which server can retrieve this zone'
        ),
        query_acl=dict(
            type='list', elements='str', required=False, default=[], aliases=['allow_query'],
            description='An ACL where you allow which client are allowed '
                        'to query this zone'
        ),
        ttl=dict(
            type='int', required=False, default=86400,
            description='The general Time To Live for this zone'
        ),
        refresh=dict(
            type='int', required=False, default=21600,
            description='The time in seconds after which name servers should '
                        'refresh the zone information'
        ),
        retry=dict(
            type='int', required=False, default=3600,
            description='The time in seconds after which name servers should '
                        'retry requests if the primary does not respond'
        ),
        expire=dict(
            type='int', required=False, default=3542400,
            description='The time in seconds after which name servers should '
                        'stop answering requests if the primary does not respond'
        ),
        negative=dict(
            type='int', required=False, default=3600,
            description='The time in seconds after which an entry for a '
                        'non-existent record should expire from cache'
        ),
        admin_mail=dict(
            type='str', required=False, default='mail.opnsense.localdomain',
            description='The mail address of zone admin. A @-sign will '
                        'automatically be replaced with a dot in the zone data'
        ),
        server=dict(
            type='str', required=False, default='opnsense.localdomain', aliases=['dns_server'],
            description='Set the DNS server hosting this file. This should usually '
                        'be the FQDN of your firewall where the BIND plugin is installed'
        ),
        # serial=dict(type='str', required=False),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Domain(m=module_input, result=result))
    return result
