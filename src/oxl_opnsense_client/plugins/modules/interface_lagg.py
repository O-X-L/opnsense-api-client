from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.interface_lagg import Lagg


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        device=dict(
            type='str', required=False, aliases=['laggif'],
            description="Optional 'device' of the entry. Needs to start with 'lagg'",
        ),
        members=dict(
            type='list', elements='str', required=False, aliases=['port', 'int', 'if', 'parent'],
            description='Existing LAGG capable interface - you must provide the network '
                        "port as shown in 'Interfaces - Assignments - Network port'"
        ),
        primary_member=dict(
            type='list', elements='str', required=False,
            description='This interface will be added first in the lagg making it the primary one '
                        "- you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
        ),
        proto=dict(
            type='str', required=False, aliases=['p'], default='lacp',
            choices=['none', 'lacp', 'failover', 'fec', 'loadbalance', 'roundrobin'],
            description="The protocol to use."
        ),
        lacp_fast_timeout=dict(type='bool', required=False, default=False, aliases=['fast_timeout'],
            description='Enable lacp fast-timeout on the interface.'
        ),
        use_flowid=dict(
            type='str', required=False, choices=['yes', 'no'], aliases=['flowid'],
            description='Use the RSS hash from the network card if available, otherwise a hash is locally calculated. '
                        'The default depends on the system tunable in net.link.lagg.default_use_flowid.'
        ),
        lagghash=dict(
            type='list', elements='str', required=False, aliases=['hash', 'hash_layers'],
            choices=['l2', 'l3', 'l4'],
            description='Set the packet layers to hash for aggregation protocols which load balance.'
        ),
        lacp_strict=dict(
            type='str', required=False,
            choices=['yes', 'no'],
            description='Enable lacp strict compliance on the interface. The default depends on the '
                        'system tunable in net.link.lagg.lacp.default_strict_mode.',
        ),
        mtu=dict(
            type='int', required=False,
            description='If you leave this field blank, the smallest mtu of this laggs children will be used.'
        ),
        description=dict(type='str', required=False, aliases=['desc', 'name']),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Lagg(m=module_input, result=result))
    return result
