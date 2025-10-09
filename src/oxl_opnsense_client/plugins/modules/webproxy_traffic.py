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
    from plugins.module_utils.main.webproxy_traffic import Traffic

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/webproxy.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/webproxy.html'


def run_module(module_input):
    module_args = dict(
        download_kb_max=dict(
            type='str', required=False, default='2048',
            aliases=['download_max', 'download', 'dl_max', 'dl'],
            description='The maximum size for downloads in kilobytes (leave empty to disable)'
        ),
        upload_kb_max=dict(
            type='str', required=False, default='1024',
            aliases=['upload_max', 'upload', 'ul_max', 'ul'],
            description='The maximum size for uploads in kilobytes (leave empty to disable)'
        ),
        throttle_kb_bandwidth=dict(
            type='str', required=False, default='1024',
            aliases=['throttle_bandwidth', 'throttle_bw', 'bandwidth', 'bw'],
            description='The allowed overall bandwidth in kilobits per second (leave empty to disable)'
        ),
        throttle_kb_host_bandwidth=dict(
            type='str', required=False, default='256',
            aliases=['throttle_host_bandwidth', 'throttle_host_bw', 'host_bandwidth', 'host_bw'],
            description='The allowed per host bandwidth in kilobits per second (leave empty to disable)'
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

    module_wrapper(Traffic(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
