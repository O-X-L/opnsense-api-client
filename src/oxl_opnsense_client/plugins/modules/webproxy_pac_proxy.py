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
        OPN_MOD_ARGS, RELOAD_MOD_ARG, STATE_ONLY_MOD_ARG
    from plugins.module_utils.main.webproxy_pac_proxy import Proxy

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/webproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/webproxy.html'


def run_module(module_input):
    module_args = dict(
        name=dict(
            type='str', required=True, description='Unique name for the proxy',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        type=dict(
            type='str', required=False, default='proxy',
            choices=['proxy', 'direct', 'http', 'https', 'socks', 'socks4', 'socks5'],
            description="Usually you should use 'direct' for a direct connection or "
                        "'proxy' for a Proxy",
        ),
        url=dict(
            type='str', required=False,
            description='A proxy URL in the form proxy.example.com:3128',
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

    module.params['type'] = module.params['type'].upper()

    module_wrapper(Proxy(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
