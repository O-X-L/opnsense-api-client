#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from basic.ansible import AnsibleModule

from plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from plugins.module_utils.base.wrapper import module_wrapper
    from plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from plugins.module_utils.main.frr_ospf_network import Network

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/frr_bgp.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/frr_bgp.html'


def run_module(module_input):
    module_args = dict(
        ip=dict(type='str', required=True, aliases=['nw_address', 'network_address', 'address']),
        mask=dict(type='int', required=True, aliases=['nw_mask', 'network_mask']),
        area=dict(
            type='str', required=False,
            description='Area in wildcard mask style like 0.0.0.0 and no decimal 0. '
                        'Only use Area in Interface tab or in Network tab once'
        ),
        area_range=dict(
            type='str', required=False,
            description='Here you can summarize a network for this area like 192.168.0.0/23'
        ),
        prefix_list_in=dict(
            type='str', required=False, aliases=['prefix_in', 'pre_in']
        ),
        prefix_list_out=dict(
            type='str', required=False, aliases=['prefix_out', 'pre_out']
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured network with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['ip', 'mask', 'area', 'area_range'],
            default=['ip', 'mask'],
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
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

    module_wrapper(Network(module=module, result=result))
    return result






if __name__ == '__main__':
    pass
