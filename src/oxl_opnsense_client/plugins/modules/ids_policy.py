from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.ids_policy import Policy


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        description=dict(type='str', required=True, aliases=['name', 'desc']),
        priority=dict(
            type='int', required=False, aliases=['prio'], default=0,
            description='Policies are processed on a first match basis a lower number means more important',
        ),
        rulesets=dict(
            type='list', elements='str', required=False, aliases=['rs'], default=[],
            description='Rulesets this policy applies to (all when none selected)',
        ),
        action=dict(
            type='list', elements='str', required=False, aliases=['a'],
            choices=['disable', 'alert', 'drop'],
            description='Rule configured action',
        ),
        new_action=dict(
            type='str', required=False, aliases=['na'], default='alert',
            choices=['default', 'disable', 'alert', 'drop'],
            description='Action to perform when filter policy applies',
        ),
        rules=dict(
            type='dict', required=False,
            description="Key-value pairs of policy-rules as provided by the enabled rulesets. "
                        "Values must be string or lists. Example: "
                        "'{\"rules\": {\"signature_severity\": [\"Minor\", \"Major\"], \"tag\": \"Dshield\"}}'",
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Policy(m=module_input, result=result))
    return result
