from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.interface_vip import Vip


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        address=dict(
            type='str', required=True, aliases=['addr', 'ip', 'network', 'net'],
            description='Provide an address and subnet to use. (e.g 192.168.0.1/24)',
        ),
        interface=dict(
            type='str', required=True, aliases=['port', 'int', 'if'],
            description='Existing interface - you must provide the network '
                        "port as shown in 'Interfaces - Assignments - Network port'"
        ),
        mode=dict(
            type='str', required=False, aliases=['m'], default='ipalias',
            choices=['ipalias', 'carp', 'proxyarp', 'other'],
        ),
        expand=dict(type='bool', required=False, default=True),
        bind=dict(
            type='bool', required=False, default=True,
            description="Assigning services to the virtual IP's interface will automatically "
                        "include this address. Uncheck to prevent binding to this address instead"
        ),
        gateway=dict(
            type='str', required=False, aliases=['gw'],
            description='For some interface types a gateway is required to configure an '
                        'IP Alias (ppp/pppoe/tun), leave this field empty for all other interface types'
        ),
        password=dict(
            type='str', required=False, aliases=['pwd'],
            description='VHID group password', no_log=True,
        ),
        vhid=dict(
            type='str', required=False, aliases=['group', 'grp', 'id'],
            description='VHID group that the machines will share'
        ),
        advertising_base=dict(
            type='int', required=False, aliases=['adv_base', 'base'], default=1,
            description='The frequency that this machine will advertise. 0 usually means master. '
                        'Otherwise the lowest combination of both values in the cluster determines the master'
        ),
        advertising_skew=dict(
            type='int', required=False, aliases=['adv_skew', 'skew'], default=0,
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured VIP with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['address', 'interface', 'cidr', 'description'],
            default=['address', 'interface'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Vip(m=module_input, result=result))
    return result
