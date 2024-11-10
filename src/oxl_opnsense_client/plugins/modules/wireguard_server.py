from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.wireguard_server import Server


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(type='str', required=True),
        public_key=dict(type='str', required=False, alises=['pubkey', 'pub']),
        private_key=dict(type='str', required=False, alises=['privkey', 'priv']),
        port=dict(type='int', required=False),
        mtu=dict(type='int', required=False, default=1420),
        dns_servers=dict(
            type='list', elements='str', required=False, default=[], aliases=['dns'],
        ),
        allowed_ips=dict(
            type='list', elements='str', required=False, default=[],
            aliases=[
                'tunnel_ips', 'tunnel_ip', 'tunneladdress', 'tunnel_adresses',
                'addresses', 'address', 'tunnel_address', 'allowed',
            ]
        ),
        disable_routes=dict(type='bool', default=False, required=False, aliases=['disableroutes']),
        gateway=dict(type='str', required=False, aliases=['gw']),
        vip=dict(
            type='str', required=False,
            aliases=['vip_depend', 'carp', 'carp_depend'],
            description='The Virtual-CARP-IP (CARP VHID) to depend on. '
                        'When this virtual address is not in master state, then the instance will be shutdown'
        ),
        peers=dict(type='list', elements='str', required=False, default=[], aliases=['clients']),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Server(m=module_input, result=result))
    return result
