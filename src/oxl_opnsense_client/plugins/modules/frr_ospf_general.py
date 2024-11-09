from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_ospf_general import General


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        carp=dict(
            type='bool', required=False, default=False, aliases=['carp_demote'],
            description='Register CARP status monitor, when no neighbors are found, '
                        'consider this node less attractive. This feature needs syslog '
                        'enabled using "Debugging" logging to catch all relevant status '
                        'events. This option is not compatible with "Enable CARP Failover"'
        ),
        id=dict(
            type='str', required=False, aliases=['router_id'],
            description='If you have a CARP setup, you may want to configure a router id '
                        'in case of a conflict'
        ),
        cost=dict(
            type='int', required=False,
            aliases=['reference_cost', 'ref_cost'],
            description='Here you can adjust the reference cost in Mbps for path calculation. '
                        'Mostly needed when you bundle interfaces to higher bandwidth'
        ),
        passive_ints=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['passive_interfaces'],
            description='Select the interfaces, where no OSPF packets should be sent to'
        ),
        redistribute=dict(
            type='list', elements='str', required=False, default=[],
            options=['bgp', 'connected', 'kernel', 'rip', 'static'],
            description='Select other routing sources, which should be '
                        'redistributed to the other nodes'
        ),
        redistribute_map=dict(
            type='str', required=False,
            description='Route Map to set for Redistribution'
        ),
        originate=dict(
            type='bool', required=False, default=False, aliases=['orig', 'advertise_default_gw'],
            description='This will send the information that we have a default gateway'
        ),
        originate_always=dict(
            type='bool', required=False, default=False,
            aliases=['orig_always', 'always_advertise_default_gw'],
            description='This will send the information that we have a default gateway, '
                        'regardless of if it is available'
        ),
        originate_metric=dict(
            type='int', required=False, aliases=['orig_metric'],
            description='This let you manipulate the metric when advertising default gateway'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(General(m=module_input, result=result))
    return result
