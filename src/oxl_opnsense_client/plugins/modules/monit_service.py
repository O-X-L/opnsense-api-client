from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.monit_service import Service


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(type='str', required=True, description='Unique service name'),
        type=dict(
            type='str', required=False,
            choices=[
                'process', 'file', 'fifo', 'filesystem', 'directory', 'host', 'system',
                'custom', 'network',
            ]
        ),
        pidfile=dict(type='path', required=False),
        match=dict(type='str', required=False),
        path=dict(
            type='path', required=False,
            description='According to the service type path can be a file or a directory',
        ),
        service_timeout=dict(type='int', required=False, default=300, aliases=['svc_timeout']),
        address=dict(
            type='str', required=False,
            description="The target IP address for 'Remote Host' and 'Network' checks",
        ),
        interface=dict(
            type='str', required=False,
            description="The existing Interface for 'Network' checks"
        ),
        start=dict(
            type='str', required=False,
            description='Absolute path to the executable with its arguments to run '
                        'at service-start',
        ),
        stop=dict(
            type='str', required=False,
            description='Absolute path to the executable with its arguments to run '
                        'at service-stop',
        ),
        tests=dict(type='list', elements='str', required=False, default=[]),
        depends=dict(
            type='list', elements='str', required=False, default=[],
            description='Optionally define a (list of) service(s) which are required '
                        'before monitoring this one, if any of the dependencies are either '
                        'stopped or unmonitored this service will stop/unmonitor too',
        ),
        polltime=dict(
            type='str',  required=False,
            description='Set the service poll time. Either as a number of cycles '
                        "'NUMBER CYCLES' or Cron-style '* 8-19 * * 1-5'"
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Service(m=module_input, result=result))
    return result
