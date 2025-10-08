from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_ospf_network import Network


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        ip=dict(type='str', required=True, aliases=['nw_address', 'network_address', 'address']),
        mask=dict(type='int', required=True, aliases=['nw_mask', 'network_mask']),
        area=dict(
            type='str', required=False,
            description='Area in wildcard mask style like 0.0.0.0 and no decimal 0. '
                        'Only use Area in Interface tab or in Network tab once'
        ),
        area_range=dict(
            type='str', required=False,
            description='Here you can summarize a network for this area like 192.168.0.0/23'
        ),
        prefix_list_in=dict(
            type='str', required=False, aliases=['prefix_in', 'pre_in']
        ),
        prefix_list_out=dict(
            type='str', required=False, aliases=['prefix_out', 'pre_out']
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured network with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['ip', 'mask', 'area', 'area_range'],
            default=['ip', 'mask'],
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Network(m=module_input, result=result))
    return result
