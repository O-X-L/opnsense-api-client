from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.dhcp_reservation_v4 import ReservationV4


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        ip=dict(
            type='str', required=True, aliases=['ip_address'],
            description='IP address to offer to the client',
        ),
        mac=dict(
            type='str', required=False, aliases=['mac_address'],
            description='MAC/Ether address of the client in question',
        ),
        subnet=dict(
            type='str', required=False,
            description='Subnet this reservation belongs to',
        ),
        hostname=dict(
            type='str', required=False,
            description='Offer a hostname to the client',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        ipv=dict(type='int', required=False, default=4, choices=[4, 6], aliases=['ip_version']),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(ReservationV4(m=module_input, result=result))
    return result
