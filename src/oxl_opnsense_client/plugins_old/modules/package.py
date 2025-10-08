from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.main.package_main import process


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    module_args = dict(
        name=dict(
            type='list', required=True, elements='str',
            description='Package or list of packages to process'
        ),
        action=dict(
            type='str', required=True,
            choices=['install', 'reinstall', 'remove', 'lock', 'unlock']
        ),
        post_sleep=dict(
            type='int', required=False, default=3,
            description='The firewall needs some time to update package info'
        ),
    )

    validate_input(i=module_input, definition=module_args)

    # todo: profiling
    process(m=m, p=m.params, r=result)

    return result
