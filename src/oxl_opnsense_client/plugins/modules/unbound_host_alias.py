#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from basic.ansible import AnsibleModule

from plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from plugins.module_utils.base.wrapper import module_wrapper
    from plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from plugins.module_utils.main.unbound_host_alias import Alias

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/unbound_host_alias.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/unbound_host_alias.html'


def run_module(module_input):
    module_args = dict(
        alias=dict(type='str', required=True, aliases=['hostname']),
        domain=dict(type='str', required=True, aliases=['dom', 'd']),
        target=dict(type='str', required=False, aliases=['tgt', 'host']),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured override-alias with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['hostname', 'domain', 'alias',  'description'],
            default=['alias', 'domain'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
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

    module_wrapper(Alias(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
