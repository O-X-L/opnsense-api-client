from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.shaper_pipe import Pipe


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        # id=dict(type='int', required=True, alises=['number']),  # ignored and set automatically
        bandwidth=dict(
            type='int', required=False, aliases=['bw']
        ),
        bandwidth_metric=dict(
            type='str', required=False, default='Mbit', aliases=['bw_metric'],
            choices=['bit', 'Kbit', 'Mbit', 'Gbit'],
        ),
        queue=dict(type='str', required=False),
        mask=dict(
            type='str', required=False, default='none', choices=['none', 'src-ip', 'dst-ip']
        ),
        buckets=dict(type='str', required=False),
        scheduler=dict(
            type='str', required=False,
            choices=['fifo', 'rr', 'qfq', 'fq_codel', 'fq_pie']
        ),
        pie_enable=dict(type='bool', required=False, default=False, aliases=['pie']),
        codel_enable=dict(type='bool', required=False, default=False, aliases=['codel']),
        codel_ecn_enable=dict(type='bool', required=False, default=False, aliases=['codel_ecn']),
        codel_target=dict(type='str', required=False),
        codel_interval=dict(type='int', required=False),
        fqcodel_quantum=dict(type='str', required=False),
        fqcodel_limit=dict(type='str', required=False),
        fqcodel_flows=dict(type='str', required=False),
        delay=dict(type='str', required=False),
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
    module_wrapper(Pipe(m=module_input, result=result))
    return result
