from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.unbound_dot import DnsOverTls


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        domain=dict(
            type='str', required=False, aliases=['dom', 'd'],
            description='Provide a domain to limit the DNS-over-TLS to or leave empty to act as a catch-all'
        ),
        target=dict(
            type='str', required=True, aliases=['tgt', 'server', 'srv'],
            description='Server to forward the dns queries to'
        ),
        port=dict(
            type='int', required=False, default=53, aliases=['p'],
            description='DNS port of the target server'
        ),
        verify=dict(
            type='str', required=False, aliases=['common_name', 'cn', 'hostname'],
            description='Verify if CN in certificate matches this value, if not set - '
                        'certificate verification will not be performed!'
        ),
        type=dict(type='str', required=False, choices=['dot'], default='dot'),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(DnsOverTls(m=module_input, result=result))
    return result
