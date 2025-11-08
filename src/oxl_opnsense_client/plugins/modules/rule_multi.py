#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from basic.ansible import AnsibleModule


from plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from plugins.module_utils.base.wrapper import \
        module_multi_wrapper
    from plugins.module_utils.base.multi import \
        build_multi_mod_args
    from plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from plugins.module_utils.defaults.rule import \
        RULE_MOD_ARGS, RULE_MATCH_FIELDS_ARG
    from plugins.module_utils.main.rule import Rule

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/rule.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/rule.html'


def run_module(module_input):
    entry_multi_args = build_multi_mod_args(
        mod_args=RULE_MOD_ARGS,
        aliases=['rules'],
    )

    module_args = dict(
        **entry_multi_args,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG,
        **RULE_MATCH_FIELDS_ARG,
    )

    module = AnsibleModule(
        module_input=module_input,
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[
            ('multi', 'multi_purge', 'multi_control.purge_all'),
        ],
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        },
    )

    module_multi_wrapper(
        module=module,
        result=result,
        obj=Rule,
        kind='rule',
        entry_args=entry_multi_args,
    )
    return result






if __name__ == '__main__':
    pass
