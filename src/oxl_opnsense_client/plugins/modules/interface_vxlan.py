from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.interface_vxlan import Vxlan


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        # device_id=dict(type='str', required=True),  # can't be configured
        interface=dict(type='str', required=False, aliases=['vxlandev', 'device', 'int']),
        id=dict(type='int', required=True, aliases=['vxlanid', 'vni']),
        local=dict(
            type='str', required=False, aliases=[
                'source_address', 'source_ip', 'vxlanlocal', 'source', 'src',
            ],
            description='The source address used in the encapsulating IPv4/IPv6 header. The address should '
                        'already be assigned to an existing interface. When the interface is configured in '
                        'unicast mode, the listening socket is bound to this address.'
        ),
        remote=dict(
            type='str', required=False, aliases=[
                'remote_address', 'remote_ip', 'destination', 'vxlanremote', 'dest',
            ],
            description='The interface can be configured in a unicast, or point-to-point, mode to create '
                        'a tunnel between two hosts. This is the IP address of the remote end of the tunnel.'
        ),
        group=dict(
            type='str', required=False, aliases=[
                'multicast_group', 'multicast_address', 'multicast_ip', 'vxlangroup',
            ],
            description='The interface can be configured in a multicast mode to create a virtual '
                        'network of hosts. This is the IP multicast group address the interface will join.'
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Vxlan(m=module_input, result=result))
    return result
