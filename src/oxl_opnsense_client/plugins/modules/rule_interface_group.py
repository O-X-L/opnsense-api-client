from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.rule_interface_group import Group


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['ifname'],
            description='Name of the interface group. Only texts containing letters, '
                        'digits and underscores with a maximum length of 15 characters '
                        'are allowed and the name may not end with a digit.',
        ),
        members=dict(
            type='list', elements='str', required=False, aliases=['ints', 'interfaces'],
            description='Member interfaces - you must provide the network '
                        "port as shown in 'Interfaces - Assignments - Network port'"
        ),
        gui_group=dict(
            type='bool', required=False, aliases=['gui'], default=True,
            description='Grouping these members in the interfaces menu section'
        ),
        sequence=dict(
            type='int', required=False, default=0, aliases=['seq'],
            description='Priority sequence used in sorting the groups '
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Group(m=module_input, result=result))
    return result
