from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.webproxy_pac_rule import Rule


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['desc', 'name'],
            description='Unique description used to identify existing rules'
        ),
        matches=dict(
            type='list', elements='str', required=False, default=[],
            description='Matches you want to use in this rule. This matches '
                        'are joined using the selected separator',
        ),
        proxies=dict(
            type='list', elements='str', required=False, default=[],
            description='Proxies you want to use address using this rule',
        ),
        join_type=dict(
            type='str', required=False, default='and',
            aliases=['join'], choices=['and', 'or'],
            description="A separator to join the matches. 'or' means any match "
                        'can be true which can be used to configure the same '
                        "proxy for multiple networks while 'and' means all matches "
                        'must be true which can be used to assign the proxy in a '
                        'more detailed way',
        ),
        match_type=dict(
            type='str', required=False, default='if',
            aliases=['operator'], choices=['if', 'unless'],
            description="Choose 'if' in case any case you want to ensure a match to "
                        "evaluate as is, else choose 'unless' if you want the negated "
                        'version. Unless is used if you want to use the proxy for every '
                        'host but not for some special ones',
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Rule(m=module_input, result=result))
    return result
