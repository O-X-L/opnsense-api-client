from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.unbound_host import Host


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        hostname=dict(type='str', required=True, aliases=['host', 'h']),
        domain=dict(type='str', required=True, aliases=['dom', 'd']),
        record_type=dict(
            type='str', required=False, aliases=['type', 'rr', 'rt'],
            choices=['A', 'AAAA', 'MX'], default='A',
        ),
        value=dict(type='str', required=False, aliases=['server', 'srv', 'mx']),
        prio=dict(
            type='int', required=False, aliases=['mxprio'], default=10,
            description='Priority that is only used for MX record types'
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured host-overrides with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=[
                'hostname', 'domain', 'record_type', 'value',
                'prio', 'description'
            ],
            default=['hostname', 'domain', 'record_type', 'value', 'prio'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Host(m=module_input, result=result))
    return result
