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
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from plugins.module_utils.main.ipsec_vti import \
        Vti

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/ipsec.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/ipsec.html'


def run_module(module_input):
    # todo: add description to parameters => VTI not found in WebUI (?!)
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['description', 'desc'],
            description='Unique name to identify the entry'
        ),
        request_id=dict(
            type='int', default=0, required=False, aliases=['req_id', 'reqid'],
            description='This might be helpful in some scenarios, like route based tunnels (VTI), but works only if '
                        'each CHILD_SA configuration is instantiated not more than once. The default uses dynamic '
                        'reqids, allocated incrementally',
        ),
        local_address=dict(
            type='str', required=False, aliases=['local_addr', 'local'],
        ),
        remote_address=dict(
            type='str', required=False, aliases=['remote_addr', 'remote'],
        ),
        local_tunnel_address=dict(
            type='str', required=False, aliases=['local_tun_addr', 'tunnel_local', 'local_tun'],
        ),
        remote_tunnel_address=dict(
            type='str', required=False, aliases=['remote_tun_addr', 'tunnel_remote', 'remote_tun'],
        ),
        local_tunnel_secondary_address=dict(
            type='str', required=False, aliases=['local_tun_sec_addr', 'tunnel_sec_local', 'local_sec_tun'],
        ),
        remote_tunnel_secondary_address=dict(
            type='str', required=False, aliases=['remote_tun_sec_addr', 'tunnel_sec_remote', 'remote_sec_tun'],
        ),
        skip_firewall=dict(
            type='bool', require=False, aliases=['skip_fw'], default=False
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

    module_wrapper(Vti(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
