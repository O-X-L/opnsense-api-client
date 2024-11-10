from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.defaults.rule import RULE_MOD_ARG_ALIASES
from ..module_utils.main.shaper_rule import Rule


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        target_pipe=dict(type='str', required=False, aliases=['pipe']),
        target_queue=dict(type='str', required=False, aliases=['queue']),
        sequence=dict(
            type='int', required=False, default=1, aliases=RULE_MOD_ARG_ALIASES['sequence']
        ),
        interface=dict(
            type='str', required=False, default='lan', aliases=RULE_MOD_ARG_ALIASES['interface'],
            description='Matching packets traveling to/from interface',
        ),
        interface2=dict(
            type='str', required=False, aliases=['int2', 'i2'],
            description='Secondary interface, matches packets traveling to/from interface '
                        '(1) to/from interface (2). can be combined with direction.',
        ),
        protocol=dict(
            type='str', required=False, default='ip', aliases=RULE_MOD_ARG_ALIASES['protocol'],
            description="Protocol like 'ip', 'ipv4', 'tcp', 'udp' and so on."
        ),
        max_packet_length=dict(
            type='int', required=False, aliases=['max_packet_len', 'packet_len', 'iplen'],
        ),
        source_invert=dict(
            type='bool', required=False, default=False,
            aliases=RULE_MOD_ARG_ALIASES['source_invert'],
        ),
        source_net=dict(
            type='list', elements='str', required=False, default='any', aliases=RULE_MOD_ARG_ALIASES['source_net'],
            description="Source ip or network, examples 10.0.0.0/24, 10.0.0.1"
        ),
        source_port=dict(
            type='str', required=False, default='any', aliases=RULE_MOD_ARG_ALIASES['source_port'],
        ),
        destination_invert=dict(
            type='bool', required=False, default=False,
            aliases=RULE_MOD_ARG_ALIASES['destination_invert'],
        ),
        destination_net=dict(
            type='list', elements='str', required=False, default='any', aliases=RULE_MOD_ARG_ALIASES['destination_net'],
            description='Destination ip or network, examples 10.0.0.0/24, 10.0.0.1'
        ),
        destination_port=dict(
            type='str', required=False, default='any',
            aliases=RULE_MOD_ARG_ALIASES['destination_port'],
        ),
        dscp=dict(
            type='list', required=False, elements='str', default=[],
            description='One or multiple DSCP values',
            choices=[
                'be', 'ef', 'af11', 'af12', 'af13', 'af21', 'af22', 'af23', 'af31', 'af32', 'af33',
                'af41', 'af42', 'af43', 'cs1', 'cs2', 'cs3', 'cs4', 'cs5', 'cs6', 'cs7',
            ]
        ),
        direction=dict(
            type='str', required=False, aliases=RULE_MOD_ARG_ALIASES['direction'],
            choices=['in', 'out'], description='Leave empty for both'
        ),
        description=dict(type='str', required=True, aliases=['desc']),
        reset=dict(
            type='bool', required=False, default=False, aliases=['flush'],
            description='If the running config should be flushed and reloaded on change - '
                        'will take some time. This might have impact on other services using '
                        'the same technology underneath (such as Captive portal)'
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Rule(m=module_input, result=result))
    return result
