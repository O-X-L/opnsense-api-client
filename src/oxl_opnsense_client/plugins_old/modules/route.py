from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.route import Route


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        gateway=dict(
            type='str', required=True, aliases=['gw'],
            description='Specify a valid existing gateway matching the networks ip protocol'
        ),
        network=dict(
            type='str', required=True, aliases=['nw', 'net'],
            description='Specify a valid network matching the gateways ip protocol'
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured routes with the running config - '
                        "if any of those fields are changed, the module will think it's a new route",
            choices=['network', 'gateway', 'description'],
            default=['network', 'gateway'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Route(m=module_input, result=result))
    return result
