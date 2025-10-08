from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.helper.main import to_digit, is_true


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    module_args = dict(
        **EN_ONLY_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=m, definition=module_args)
    result['diff']['after'] = {'enabled': m.params['enabled']}

    is_enabled = is_true(
        m.c.session.get(cnf={
            'module': 'quagga',
            'controller': 'bfd',
            'command': 'get',
        })['bfd']['enabled']
    )
    result['diff']['before']['enabled'] = is_enabled

    if is_enabled != m.params['enabled']:
        result['changed'] = True

        if not m.check_mode:
            m.c.session.post(cnf={
                'module': 'quagga',
                'controller': 'bfd',
                'command': 'set',
                'data': {'bfd': {'enabled': to_digit(m.params['enabled'])}}
            })
            m.c.session.post(cnf={
                'module': 'quagga',
                'controller': 'service',
                'command': 'reconfigure',
            })

    return result
