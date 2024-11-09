from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.wireguard_peer import Peer


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(type='str', required=True),
        public_key=dict(type='str', required=False, alises=['pubkey', 'pub']),
        psk=dict(type='str', required=False),
        allowed_ips=dict(
            type='list', elements='str', required=False, default=[],
            aliases=[
                'tunnel_ips', 'tunnel_ip', 'tunneladdress', 'tunnel_adresses',
                'addresses', 'address', 'tunnel_address', 'allowed',
            ]
        ),
        server=dict(
            type='str', required=False,
            aliases=['target', 'server_address', 'serveraddress', 'endpoint']
        ),
        port=dict(type='int', required=False),
        keepalive=dict(type='int', required=False),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Peer(m=module_input, result=result))
    return result
