from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.ids_rule import Rule


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        sid=dict(
            type='int', required=True, aliases=['id'],
            description='Unique signature-ID of the rule you want to modify'
        ),
        action=dict(
            type='str', required=False, aliases=['a'], default='alert',
            choices=['alert', 'drop'],
            description='Set action to perform here, only used when in IPS mode',
        ),
        **EN_ONLY_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Rule(m=module_input, result=result))
    return result
