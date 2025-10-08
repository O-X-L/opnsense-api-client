from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.syslog import Syslog


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['hostname', 'tgt', 'server', 'srv'],
            description='Server to forward the logs to'
        ),
        port=dict(type='int', required=False, default=514, aliases=['p']),
        transport=dict(
            type='str', required=False, default='udp4', aliases=['trans', 't'],
            choices=['udp4', 'tcp4', 'udp6', 'tcp6', 'tls4', 'tls6'],
        ),
        level=dict(
            type='list', required=False, aliases=['lv', 'lvl'], elements='str',
            default=['info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg'],
            choices=['debug', 'info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg'],
        ),
        program=dict(
            type='list', required=False, aliases=['prog'], default=[], elements='str',
            description='Limit applications to send logs from'
        ),
        facility=dict(
            type='list', required=False, aliases=['fac'], default=[], elements='str',
            choices=[
                'kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news', 'uucp', 'cron', 'authpriv',
                'ftp', 'ntp', 'security', 'console', 'local0', 'local1', 'local2', 'local3', 'local4',
                'local5', 'local6', 'local7',
            ],
        ),
        certificate=dict(type='str', required=False, aliases=['cert']),
        rfc5424=dict(type='bool', required=False, default=False),  # not getting current value from response
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured syslog-destinations with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=[
                'target', 'transport', 'facility', 'program', 'level',
                'port', 'description',
            ],
            default=['target', 'facility', 'program'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Syslog(m=module_input, result=result))
    return result
