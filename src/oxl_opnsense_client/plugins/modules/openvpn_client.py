from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.defaults.openvpn import OPENVPN_INSTANCE_MOD_ARGS
from ..module_utils.main.openvpn_client import Client


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        # general
        remote=dict(
            type='list', elements='str', required=False, aliases=['peer', 'server'],
            description='Remote host name or IP address with optional port'
        ),
        port=dict(
            type='int', required=False, aliases=['local_port', 'bind_port'],
            description='Port number to use.'
                        'Specifies a bind address, or nobind when client does not have a specific bind address.'
        ),
        carp_depend_on=dict(
            aliases=['vip', 'vip_depend', 'carp', 'carp_depend'],
            type='str', required=False,
            description='The carp VHID to depend on, when this virtual address is not in '
                        'master state, the interface cost will be set to the demoted cost'
        ),
        # auth
        username=dict(
            type='str', required=False, aliases=['user'],
            description='(optional) Username to send to the server for authentication when required.'
        ),
        password=dict(
            type='str', required=False, aliases=['pwd'], no_log=True,
            description='Password belonging to the user specified above'
        ),
        **OPENVPN_INSTANCE_MOD_ARGS,
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Client(m=module_input, result=result))
    return result
