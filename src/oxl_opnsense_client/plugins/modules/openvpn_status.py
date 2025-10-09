#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from basic.ansible import AnsibleModule

from plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS
    from plugins.module_utils.base.api import single_get

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/openvpn.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/openvpn.html'

TARGET_MAPPING = {
    'sessions': 'searchSessions',
    'routes': 'searchRoutes',
}


def run_module(module_input):
    module_args = dict(
        target=dict(
            type='str', required=False, default='sessions', aliases=['kind'],
            choices=['sessions', 'routes'],
            description='What information to query'
        ),
        **OPN_MOD_ARGS,
    )

    module = AnsibleModule(
        module_input=module_input,
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info = single_get(
        module=module,
        cnf={
            'module': 'openvpn',
            'controller': 'service',
            'command': TARGET_MAPPING[module.params['target']],
        }
    )

    if 'rows' in info:
        info = info['rows']

        if isinstance(info, str):
            info = info.strip()

    return info






if __name__ == '__main__':
    pass
