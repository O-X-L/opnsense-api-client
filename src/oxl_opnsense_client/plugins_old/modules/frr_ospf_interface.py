from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_ospf_interface import Interface


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        interface=dict(type='str', required=True, aliases=['name', 'int']),
        auth_type=dict(type='str', required=False, choices=['message-digest']),
        auth_key=dict(type='str', required=False, no_log=True),
        auth_key_id=dict(type='int', required=False, default=1),
        area=dict(
            type='str', required=False,
            description='Area in wildcard mask style like 0.0.0.0 and no decimal 0'
        ),
        cost=dict(type='int', required=False),
        cost_demoted=dict(type='int', required=False, default=65535),
        carp_depend_on=dict(
            type='str', required=False,
            description='The carp VHID to depend on, when this virtual address is not in '
                        'master state, the interface cost will be set to the demoted cost'
        ),
        hello_interval=dict(type='int', required=False, aliases=['hello']),
        dead_interval=dict(type='int', required=False, aliases=['dead']),
        retransmit_interval=dict(type='int', required=False, aliases=['retransmit']),
        transmit_delay=dict(type='int', required=False, aliases=['delay']),
        priority=dict(type='int', required=False, aliases=['prio']),
        network_type=dict(
            type='str', required=False, aliases=['nw_type'],
            choices=['broadcast', 'non-broadcast', 'point-to-multipoint', 'point-to-point'],
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured interface with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['interface', 'area', 'passive', 'carp_depend_on', 'network_type'],
            default=['interface', 'area'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Interface(m=module_input, result=result))
    return result
