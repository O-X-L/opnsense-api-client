from ..base.handler import ModuleSoftError
from ..defaults.alias import ALIAS_DEFAULTS, ALIAS_MOD_ARGS, ALIAS_MOD_ARG_ALIASES
from ..helper.main import diff_remove_empty, ensure_list
from ..helper.multi import validate_single, convert_aliases
from ..main.alias import Alias


# pylint: disable=R0915
def process(m, p: dict, r: dict, ) -> None:
    meta_alias = Alias(m=m, result={})
    existing_aliases = meta_alias.get_existing()

    defaults = {}
    overrides = {
        'debug': p['debug'],
        'firewall': p['firewall'],
    }

    if p['state'] is not None:
        defaults['state'] = p['state']

    if p['enabled'] is not None:
        defaults['enabled'] = p['enabled']

    # build list of valid aliases or fail if invalid config is not permitted
    valid_aliases = []
    for alias_name, alias_config in p['aliases'].items():
        # build config and validate it the same way the module initialization would do
        if alias_config is None:
            alias_config = {}

        alias_config = convert_aliases(cnf=alias_config, aliases=ALIAS_MOD_ARG_ALIASES)

        real_cnf = {
            **ALIAS_DEFAULTS,
            **defaults,
            **alias_config,
            'name': alias_name,
            **overrides,
        }
        real_cnf['content'] = list(map(str, ensure_list(real_cnf['content'])))

        if real_cnf['debug']:
            m.warn(f"Validating alias: '{alias_config}'")

        if validate_single(
                m=m, module_args=ALIAS_MOD_ARGS, log_mod='alias',
                key=alias_name, cnf=real_cnf,
        ):
            valid_aliases.append(real_cnf)

    for alias_config in valid_aliases:
        # process single alias like in the 'alias' module
        alias_result = dict(
            changed=False,
            diff={
                'before': {},
                'after': {},
            }
        )

        p['debug'] = alias_config['debug']  # per alias switch

        if p['debug'] or p['output_info']:
            m.warn(f"Processing alias: '{alias_config}'")

        try:
            alias = Alias(
                m=m,
                result=alias_result,
                cnf=alias_config,
                fail_verify=p['fail_verification'],
                fail_proc=p['fail_processing'],
            )
            # save on requests
            alias.existing_entries = existing_aliases

            alias.check()
            alias.process()

            if alias_result['changed']:
                r['changed'] = True
                alias_result['diff'] = diff_remove_empty(alias_result['diff'])

                if 'before' in alias_result['diff']:
                    r['diff']['before'].update(alias_result['diff']['before'])

                if 'after' in alias_result['diff']:
                    r['diff']['after'].update(alias_result['diff']['after'])

        except ModuleSoftError:
            continue

    if r['changed'] and p['reload']:
        meta_alias.reload()
