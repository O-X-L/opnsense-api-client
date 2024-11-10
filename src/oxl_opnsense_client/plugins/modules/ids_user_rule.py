from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.ids_user_rule import Rule


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['name', 'desc'],
            description='Unique rule name',
        ),
        source_ip=dict(
            type='str', required=False, aliases=['source', 'src_ip', 'src'],
            description="Set the source IP or network to match. Leave this field empty for using 'any'",
        ),
        destination_ip=dict(
            type='str', required=False, aliases=['destination', 'dst_ip', 'dst'],
            description="Set the destination IP or network to match. Leave this field empty for using 'any'",
        ),
        ssl_fingerprint=dict(
            type='str', required=False, aliases=['fingerprint', 'ssl_fp'],
            description="The SSL fingerprint, for example: "
                        "'B5:E1:B3:70:5E:7C:FF:EB:92:C4:29:E5:5B:AC:2F:AE:70:17:E9:9E'",
        ),
        action=dict(
            type='str', required=False, aliases=['a'], default='alert',
            choices=['alert', 'drop', 'pass'],
            description='Set action to perform here, only used when in IPS mode',
        ),
        bypass=dict(
            type='bool', required=False, aliases=['bp'], default=False,
            description='Set bypass keyword. Increases traffic throughput. Suricata reads a packet, '
                        'decodes it, checks it in the flow table. If the corresponding flow is local '
                        'bypassed then it simply skips all streaming, detection and output and the packet '
                        'goes directly out in IDS mode and to verdict in IPS mode',
        ),
        **STATE_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Rule(m=module_input, result=result))
    return result
