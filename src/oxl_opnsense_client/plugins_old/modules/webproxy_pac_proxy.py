from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.webproxy_pac_proxy import Proxy


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(
            type='str', required=True, description='Unique name for the proxy',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        type=dict(
            type='str', required=False, default='proxy',
            choices=['proxy', 'direct', 'http', 'https', 'socks', 'socks4', 'socks5'],
            description="Usually you should use 'direct' for a direct connection or "
                        "'proxy' for a Proxy",
        ),
        url=dict(
            type='str', required=False,
            description='A proxy URL in the form proxy.example.com:3128',
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Proxy(m=module_input, result=result))
    return result
