from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.main.savepoint import SavePoint


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    module_args = dict(
        action=dict(
            type='str', required=False, default='create',
            choices=['create', 'revert', 'apply', 'cancel_rollback', 'cancel'],
        ),
        revision=dict(
            type='str', required=False,
            description='Savepoint revision to apply, revert or cancel_rollback'
        ),
        controller=dict(
            type='str', required=False, default='filter', description='Target API controller',
            choices=['source_nat', 'filter']
        ),
        api_module=dict(type='str', required=False, default='firewall', choices=['firewall']),
    )

    validate_input(i=module_input, definition=module_args)

    sp = SavePoint(m=m, result=result)

    if m.params['action'] == 'create':
        result['revision'] = sp.create()

    else:
        if m.params['revision'] is None:
            m.fail('You need to provide a revision to execute this action!')

        if m.params['action'] == 'apply':
            sp.apply()

        elif m.params['action'] == 'revert':
            sp.revert()

        else:
            sp.cancel_rollback()

    return result
