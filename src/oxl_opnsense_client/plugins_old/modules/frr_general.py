from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_general import General


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        carp=dict(
            type='bool', required=False, default=False, aliases=['carp_failover'],
            description='Will activate the routing service only on the primary device'
        ),
        profile=dict(
            type='str', required=False, default='traditional',
            options=['traditional', 'datacenter'],
            description="The 'datacenter' profile is more aggressive. "
                        "Please refer to the FRR documentation for more information"
        ),
        snmp_agentx=dict(
            type='bool', required=False, default=False,
            description='En- or disable support for Net-SNMP AgentX'
        ),
        log=dict(
            type='bool', required=False, default=True, aliases=['logging'],
        ),
        log_level=dict(
            type='str', required=False, default='notifications',
            options=[
                'critical', 'emergencies', 'errors', 'alerts', 'warnings', 'notifications',
                'informational', 'debugging',
            ],
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(General(m=module_input, result=result))
    return result
