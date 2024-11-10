from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.ipsec_vti import Vti


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

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
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Vti(m=module_input, result=result))
    return result
