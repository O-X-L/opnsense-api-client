from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG
from ..module_utils.main.frr_bfd_neighbor import Neighbor


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        ip=dict(type='str', required=True, aliases=[
            'neighbor', 'peer', 'peer_ip', 'address',
        ]),
        description=dict(type='str', required=False, aliases=['desc']),
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Neighbor(m=module_input, result=result))
    return result
