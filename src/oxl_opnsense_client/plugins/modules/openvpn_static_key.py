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
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from plugins.module_utils.main.openvpn_static_key import Key

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/openvpn.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/openvpn.html'

def run_module(module_input):
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['desc', 'description'],
            description='The name used to match this config to existing entries'
        ),
        mode=dict(
            type='str', required=False, default='crypt', aliases=['type'], choices=['auth', 'crypt'],
            description='Define the use of this key, authentication (--tls-auth) or authentication and '
                        'encryption (--tls-crypt)'
        ),
        key=dict(
            type='str', required=False, no_log=True,
            description='OpenVPN Static key. If empty - it will be auto-generated.'
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

    module_wrapper(Key(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
