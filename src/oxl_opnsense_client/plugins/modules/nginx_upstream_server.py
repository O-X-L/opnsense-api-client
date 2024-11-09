from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import RELOAD_MOD_ARG_DEF_FALSE, STATE_ONLY_MOD_ARG
from ..module_utils.main.nginx_upstream_server import UpstreamServer


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        description=dict(type='str', alias=['name'], required=True, aliases=['name']),
        server=dict(type='str', required=False),
        port=dict(type='int', required=False),
        priority=dict(type='int', required=False),
        max_conns=dict(type='int', required=False),
        max_fails=dict(type='int', required=False),
        fail_timeout=dict(type='int', required=False),
        no_use=dict(
            type='str', required=False, choices=['', 'down', 'backup'], default='',
        ),
        **RELOAD_MOD_ARG_DEF_FALSE,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(UpstreamServer(m=module_input, result=result))
    return result
