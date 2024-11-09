from ..module_input import validate_input, ModuleInput, valid_results


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    module_args = dict(
        target=dict(
            type='str', required=True,
            choices=[
                'bgpneighbors', 'bgproute', 'bgproute4', 'bgproute6', 'bgpsummary',
                'generalroute', 'generalroute4', 'generalroute6', 'generalrunningconfig',
                'ospfdatabase', 'ospfinterface', 'ospfneighbor', 'ospfoverview', 'ospfroute',
                'ospfv3database', 'ospfv3interface', 'ospfv3neighbor', 'ospfv3overview',
                'ospfv3route',
            ],
            description='What information to query'
        ),
    )

    validate_input(i=module_input, definition=module_args)

    non_json = ['generalrunningconfig']

    if m.params['target'] in non_json:
        params = []

    else:
        params = ['$format=”json”']

    info = m.c.session.get(
        cnf={
            'module': 'quagga',
            'controller': 'diagnostics',
            'command': m.params['target'],
            'params': params,
        }
    )

    if 'response' in info:
        info = info['response']

        if isinstance(info, str):
            info = info.strip()

    return result
