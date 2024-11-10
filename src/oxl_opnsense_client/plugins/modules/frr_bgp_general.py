from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.frr_bgp_general import General


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        as_number=dict(type='int', required=True, aliases=['as', 'as_nr']),
        id=dict(type='str', required=False, aliases=['router_id']),
        graceful=dict(
            type='bool', required=False, default=False,
            description='BGP graceful restart functionality as defined in '
                        'RFC-4724 defines the mechanisms that allows BGP speaker '
                        'to continue to forward data packets along known routes '
                        'while the routing protocol information is being restored'
        ),
        networks=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['nets'],
            description='Select the network to advertise, you have to set a '
                        'Null route via System -> Routes'
        ),
        redistribute=dict(
            type='list', elements='str', required=False, default=[],
            options=['ospf', 'connected', 'kernel', 'rip', 'static'],
            description='Select other routing sources, which should be '
                        'redistributed to the other nodes'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(General(m=module_input, result=result))
    return result
