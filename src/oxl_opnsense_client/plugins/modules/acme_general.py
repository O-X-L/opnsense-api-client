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
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG
    from plugins.module_utils.main.acme_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/en/latest/modules/acmeclient.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/en/latest/modules/acmeclient.html'


def run_module(module_input):
    module_args = dict(
        auto_renewal=dict(
            type='bool', required=False, default=True,
            description='Enable automatic renewal for certificates to prevent expiration. This will add a cron job '
                        'to the system.',
        ),
        challenge_port=dict(
            type='int', required=False, default=43580,
            description='When using HTTP-01 as challenge type, a local webserver is used to provide acme challenge '
                        'data to the ACME CA. The local webserver is NOT directly exposed to the outside and should '
                        'NOT use port 80 or any other well-known port. This setting allows you to change the local '
                        'port of this webserver in case it interferes with another local service.',
        ),
        tls_challenge_port=dict(
            type='int', required=False, default=43581,
            description='The service port when using TLS-ALPN-01 as challenge type. It works similar to the HTTP-01 '
                        'challenge type.',
        ),
        restart_timeout=dict(
            type='int', required=False, default=600,
            description='The maximum time in seconds to wait for an automation to complete. When the timeout is '
                        'reached the command is forcefully aborted.',
        ),
        haproxy_integration=dict(
            type='bool', required=False, default=False,
            description='Enable automatic integration with the OPNsense HAProxy plugin.',
        ),
        log_level=dict(
            type='str', required=False, default='normal',
            choices=['normal', 'extended', 'debug', 'debug2', 'debug3'],
            description='Specifies the log level for acme.sh.',
        ),
        show_intro=dict(
            type='bool', required=False, default=True,
            description='Disable to hide all introduction pages.',
        ),
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
