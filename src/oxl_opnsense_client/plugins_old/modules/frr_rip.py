from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_rip import Rip


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        version=dict(type='int', required=False, default=2, aliases=['v']),
        metric=dict(
            type='int', required=False, aliases=['m', 'default_metric'],
            description='Set the default metric to a value between 1 and 16'
        ),
        passive_ints=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['passive_interfaces'],
            description='Select the interfaces, where no RIP packets should be sent to'
        ),
        networks=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['nets'],
            description='Enter your networks in CIDR notation'
        ),
        redistribute=dict(
            type='list', elements='str', required=False, default=[],
            options=['bgp', 'ospf', 'connected', 'kernel', 'static'],
            description='Select other routing sources, which should be '
                        'redistributed to the other nodes'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Rip(m=module_input, result=result))
    return result
