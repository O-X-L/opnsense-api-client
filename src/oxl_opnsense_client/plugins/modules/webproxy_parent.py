#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from basic.ansible import AnsibleModule

from plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from plugins.module_utils.base.wrapper import module_wrapper
    from plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from plugins.module_utils.main.webproxy_parent import Parent

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/webproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/webproxy.html'


def run_module(module_input):
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

    module_wrapper(Parent(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
