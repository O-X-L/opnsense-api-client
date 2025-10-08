from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.monit_test import Test


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        name=dict(type='str', required=True, description='Unique test name'),
        type=dict(
            type='str', required=False, default='Custom',
            choices=[
                'Existence', 'SystemResource', 'ProcessResource', 'ProcessDiskIO',
                'FileChecksum', 'Timestamp', 'FileSize', 'FileContent', 'FilesystemMountFlags',
                'SpaceUsage', 'InodeUsage', 'DiskIO', 'Permisssion', 'UID', 'GID', 'PID', 'PPID',
                'Uptime', 'ProgramStatus', 'NetworkInterface', 'NetworkPing', 'Connection', 'Custom',
            ],
            description='Custom will not be idempotent - will be translated on the server-side. '
                        "See 'list' module output for details"
        ),
        condition=dict(
            type='str', required=False,
            description="The test condition. Per example: "
                        "'cpu is greater than 50%' or "
                        "'failed host 127.0.0.1 port 22 protocol ssh'"
        ),
        action=dict(
            type='str', required=False, default='alert',
            choices=['alert', 'restart', 'start', 'stop', 'exec', 'unmonitor']
        ),
        path=dict(
            type='path', required=False,
            description='The absolute path to the script to execute - if action is '
                        "set to 'execute'. "
                        "Make sure the script is executable by the Monit service"
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Test(m=module_input, result=result))
    return result
