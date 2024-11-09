from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.unbound_domain import Domain


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        domain=dict(type='str', required=True, aliases=['dom', 'd']),
        server=dict(
            type='str', required=True, aliases=['value', 'srv'],
            description='IP address of the authoritative DNS server for this domain. '
                        "To use a non-default port for communication, append an '@' with the port number",
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured domain-overrides with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['domain', 'server', 'description'],
            default=['domain', 'server'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Domain(m=module_input, result=result))
    return result
