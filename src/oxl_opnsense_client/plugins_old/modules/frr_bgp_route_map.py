from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_bgp_route_map import RouteMap


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        description=dict(type='str', required=False, aliases=['desc']),
        name=dict(type='str', required=True),
        action=dict(type='str', required=False, options=['permit', 'deny']),
        id=dict(
            type='int', required=False,
            description='Route-map ID between 10 and 99. Be aware that the sorting '
                        'will be done under the hood, so when you add an entry between '
                        "it get's to the right position"
        ),
        as_path_list=dict(
            type='list', elements='str', required=False, default=[], aliases=['as_path']
        ),
        prefix_list=dict(
            type='dict', required=False, default={}, aliases=['prefix', 'pre'],
            description='Dictionary of prefixes to link. Per example: '
                        "\"{prefix_name: [seq1, seq2]}\" or \"{'pre1': [5, 6]}\" will link "
                        "prefixes with the name 'pre1' and sequence 5-6"
        ),
        community_list=dict(
            type='list', elements='str', required=False, default=[], aliases=['community']
        ),
        set=dict(
            type='str', required=False,
            description='Free text field for your set, please be careful! '
                        'You can set e.g. "local-preference 300" or "community 1:1" '
                        '(http://www.nongnu.org/quagga/docs/docs-multi/'
                        'Route-Map-Set-Command.html#Route-Map-Set-Command)'
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(RouteMap(m=module_input, result=result))
    return result
