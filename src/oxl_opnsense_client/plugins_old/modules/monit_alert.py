from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.monit_alert import Alert


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        recipient=dict(
            type='str', required=True, aliases=['email', 'mail'],
            description='The email address to send alerts to',
        ),
        not_on=dict(
            type='bool', required=False, default=False, aliases=['not'],
            description='Do not send alerts for the following events but on all others',
        ),
        events=dict(
            type='list', elements='str', required=False, default=[],
            choices=[
                'action', 'checksum', 'bytein', 'byteout', 'connection', 'content',
                'data', 'exec', 'fsflags', 'gid', 'icmp', 'instance', 'invalid',
                'link', 'nonexist', 'packetin', 'packetout', 'permission', 'pid',
                'ppid', 'resource', 'saturation', 'size',  'speed', 'status',
                'timeout', 'timestamp', 'uid', 'uptime'
            ],
            description="Values: "
                        "'action' = 'Action done', "
                        "'checksum' = 'Checksum failed', "
                        "'bytein' = 'Download bytes exceeded', "
                        "'byteout' = 'Upload bytes exceeded', "
                        "'connection' = 'Connection failed', "
                        "'content' = 'Content failed', "
                        "'data' = 'Data access error', "
                        "'exec' = 'Execution failed', "
                        "'fsflags' = 'Filesystem flags failed', "
                        "'gid' = 'GID failed', "
                        "'icmp' = 'Ping failed', "
                        "'instance' = 'Monit instance changed', "
                        "'invalid' = 'Invalid type', "
                        "'link' = 'Link down', "
                        "'nonexist' = 'Does not exist', "
                        "'packetin' = 'Download packets exceeded', "
                        "'packetout' = 'Upload packets exceeded', "
                        "'permission' = 'Permission failed', "
                        "'pid' = 'PID failed', "
                        "'ppid' = 'PPID failed', "
                        "'resource' = 'Resource limit matched', "
                        "'saturation' = 'Saturation exceeded', "
                        "'size' = 'Size failed', "
                        "'speed' = 'Speed failed', "
                        "'status' = 'Status failed', "
                        "'timestamp' = 'Timestamp failed', "
                        "'uid' = 'UID failed', "
                        "'uptime' = 'Uptime failed'"
        ),
        format=dict(
            type='str', required=False,
            description='The email format for alerts. Subject: $SERVICE on $HOST failed'
        ),
        reminder=dict(
            type='int', required=False, default=10,
            description='Send a reminder after some cycles',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured alerts with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['recipient', 'not_on', 'events', 'reminder', 'description'],
            default=['recipient'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Alert(m=module_input, result=result))
    return result
