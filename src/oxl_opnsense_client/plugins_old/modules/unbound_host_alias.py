from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.unbound_host_alias import Alias


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        alias=dict(type='str', required=True, aliases=['hostname']),
        domain=dict(type='str', required=True, aliases=['dom', 'd']),
        target=dict(type='str', required=False, aliases=['tgt', 'host']),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured override-alias with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['hostname', 'domain', 'alias',  'description'],
            default=['alias', 'domain'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Alias(m=module_input, result=result))
    return result
