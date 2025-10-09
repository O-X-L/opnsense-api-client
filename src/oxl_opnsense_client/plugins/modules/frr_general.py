#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from basic.ansible import AnsibleModule

from plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from plugins.module_utils.base.wrapper import module_wrapper
    from plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from plugins.module_utils.main.frr_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/frr_general.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/frr_general.html'


def run_module(module_input):
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
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        module_input=module_input,
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(General(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
