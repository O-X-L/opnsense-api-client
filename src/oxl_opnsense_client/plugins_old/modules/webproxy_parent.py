from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.webproxy_parent import Parent


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        host=dict(
            type='str', required=False, aliases=['ip'],
            description='Parent proxy IP address or hostname'
        ),
        auth=dict(
            type='bool', required=False, default=False,
            description='Enable authentication against the parent proxy'
        ),
        user=dict(
            type='str', required=False, default='placeholder',
            description='Set a username if parent proxy requires authentication'
        ),
        password=dict(
            type='str', required=False, default='placeholder', no_log=True,
            description='Set a username if parent proxy requires authentication'
        ),
        port=dict(type='int', required=False, aliases=['p']),
        local_domains=dict(
            type='list', elements='str', required=False, default=[], aliases=['domains'],
            description='Domains not to be sent via parent proxy'
        ),
        local_ips=dict(
            type='list', elements='str', required=False, default=[], aliases=['ips'],
            description='IP addresses not to be sent via parent proxy'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Parent(m=module_input, result=result))
    return result
