from ..module_input import ModuleInput, valid_results


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)
    info = module_input.c.session.get(
        cnf={
            'module': 'wireguard',
            'controller': 'service',
            'command': 'show',
        }
    )

    if 'response' in info:
        info = info['response']

        if isinstance(info, str):
            info = info.strip()

        result['info'] = info

    return result
