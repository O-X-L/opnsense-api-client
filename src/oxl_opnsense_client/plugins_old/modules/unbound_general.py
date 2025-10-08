from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.unbound_general import General


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        port=dict(
            type='int', required=False, default=53,
            description='The TCP/UDP port used for responding to DNS queries'
        ),
        interfaces=dict(
            type='list', elements='str', required=False, default=[],
            description='The interface(s) used for responding to queries from clients'
        ),
        dnssec=dict(
            type='bool', required=False, default=False,
            description='Whether DNSSEC is enabled'
        ),
        dns64=dict(
            type='bool', required=False, default=False,
            description='Whether Unbound will synthesize AAAA records from A records if no '
                        'actual AAAA records are present'
        ),
        # IPv6 netmask
        dns64_prefix=dict(
            type='str', required=False, default='64:ff9b::/96',
            description='The DNS64 prefix'
        ),
        aaaa_only_mode=dict(
            type='bool', required=False, default=False,
            description='Whether Unbound will remove all A records from the answer section '
                        'of all responses'
        ),
        register_dhcp_leases=dict(
            type='bool', required=False, default=False,
            description='Whether machines that specify their hostname when requesting a '
                        'DHCP lease will be registered in Unbound'
        ),
        dhcp_domain=dict(
            type='str', required=False,
            description='The default domain name to use for DHCP lease registration'
        ),
        register_dhcp_static_mappings=dict(
            type='bool', required=False, default=False,
            description='Whether DHCP static mappings will be registered in Unbound'
        ),
        register_ipv6_link_local=dict(
            type='bool', required=False, default=True,
            description='Whether IPv6 link-local addresses will be registered in Unbound'
        ),
        register_system_records=dict(
            type='bool', required=False, default=True,
            description='Whether A/AAAA records for the configured listen interfaces '
                        'will be generated'
        ),
        txt_records=dict(
            type='bool', required=False, default=False, aliases=['txt'],
            description='Whether descriptions associated with Host entries and DHCP Static '
                        'mappings will create a corresponding TXT record'
        ),
        flush_dns_cache=dict(
            type='bool', required=False, default=False,
            description='Whether the DNS cache will be flushed during each daemon reload'
        ),
        local_zone_type=dict(
            type='str', required=False, default='transparent', choices=[
                'transparent', 'always_nxdomain', 'always_refuse', 'always_transparent', 'deny', 'inform',
                'inform_deny', 'nodefault', 'refuse', 'static', 'typetransparent',
            ],
            description='The local zone type used for the system domain'
        ),
        outgoing_interfaces=dict(
            type='list', elements='str', required=False, default=[],
            description='The interface(s) that Unbound will use to send queries to '
                        'authoritative servers and receive their replies'
        ),
        wpad=dict(
            type='bool', required=False, default=False,
            description='Whether CNAME records for the WPAD host of all configured domains '
                        'will be automatically added as well as overrides for TXT records for domains'
        ),
        **EN_ONLY_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(General(m=module_input, result=result))
    return result
