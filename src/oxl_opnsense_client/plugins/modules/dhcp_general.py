#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/nginx.html

from basic.ansible import AnsibleModule

from plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS
from plugins.module_utils.base.wrapper import module_wrapper

try:
    from plugins.module_utils.defaults.main import \
        EN_ONLY_MOD_ARG, OPN_MOD_ARGS, RELOAD_MOD_ARG
    from plugins.module_utils.main.dhcp_general import General


except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dhcp.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dhcp.html'


def run_module(module_input):
    module_args = dict(
        interfaces=dict(
            type='list', elements='str', required=False, default=[], aliases=['ints'],
            description='Comma separated list of network interfaces to listen on for DHCP requests'
        ),
        socket_type=dict(
            type='str', required=False, default='raw', choices=['raw', 'udp'], aliases=['dhcp_socket_type'],
            description='Socket type used for DHCP communication',
        ),
        fw_rules=dict(
            type='bool', required=False, default=True, aliases=['fwrules', 'rules'],
            description='Automatically add a basic set of firewall rules to allow dhcp traffic, '
                        'more fine grained controls can be offered manually when disabling this option',
        ),
        lifetime=dict(
            type='int', required=False, default=4000, aliases=['valid_lifetime'],
            description='Defines how long the addresses (leases) given out by the server are valid (in seconds)',
        ),
        **EN_ONLY_MOD_ARG,
        **RELOAD_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    module = AnsibleModule(
        module_input=module_input,
        argument_spec=module_args,
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module_wrapper(General(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
