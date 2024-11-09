from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_bgp_as_path import AsPath


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        description=dict(type='str', required=True, aliases=['desc']),
        number=dict(
            type='str', required=False, aliases=['nr'],
            description='The ACL rule number (10-99); keep in mind that there are no '
                        'sequence numbers with AS-Path lists. When you want to add a '
                        'new line between you have to completely remove the ACL!'
        ),
        action=dict(type='str', required=False, options=['permit', 'deny']),
        as_pattern=dict(
            type='str', required=False, aliases=['as'],
            description="The AS pattern you want to match, regexp allowed (e.g. .$ or _1$). "
                        "It's not validated so please be careful!"
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(AsPath(m=module_input, result=result))
    return result
