from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.unbound_forward import Forward


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        domain=dict(
            type='str', required=False, aliases=['dom', 'd'],
            description='Domain of the host. All queries for this domain will be forwarded to the nameserver '
                        'specified. Leave empty to catch all queries and forward them to the nameserver'
        ),
        target=dict(
            type='str', required=True, aliases=['tgt', 'server', 'srv'],
            description='Server to forward the dns queries to'
        ),
        port=dict(
            type='int', required=False, default=53, aliases=['p'],
            description='DNS port of the target server'
        ),
        type=dict(type='str', required=False, choices=['forward'], default='forward'),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Forward(m=module_input, result=result))
    return result
