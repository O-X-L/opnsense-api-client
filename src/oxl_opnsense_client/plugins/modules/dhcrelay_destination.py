#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/dhcrelay.html

from basic.ansible import AnsibleModule

from plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from plugins.module_utils.base.wrapper import module_wrapper
    from plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from plugins.module_utils.main.dhcrelay_destination import \
        DhcRelayDestination

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dhcrelay_destination.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dhcrelay_destination.html'


def run_module(module_input):
    module_args = dict(
        name=dict(
            type='str', required=True,
            description='A unique name for this relay destination.',
        ),
        server=dict(
            type='list', elements='str', required=False,
            description='A list of server IP addresses to relay DHCP requests to.'
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
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

    module_wrapper(DhcRelayDestination(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
