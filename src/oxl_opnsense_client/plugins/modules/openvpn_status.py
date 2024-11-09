from ..module_input import validate_input, ModuleInput, valid_results

TARGET_MAPPING = {
    'sessions': 'searchSessions',
    'routes': 'searchRoutes',
}


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    module_args = dict(
        target=dict(
            type='str', required=False, default='sessions', aliases=['kind'],
            choices=['sessions', 'routes'],
            description='What information to query'
        ),
    )

    validate_input(i=module_input, definition=module_args)

    info = m.c.session.get(
        cnf={
            'module': 'openvpn',
            'controller': 'service',
            'command': TARGET_MAPPING[m.params['target']],
        }
    )

    if 'rows' in info:
        info = info['rows']

        if isinstance(info, str):
            info = info.strip()

    return result
