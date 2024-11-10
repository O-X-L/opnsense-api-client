from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.cron import CronJob


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        description=dict(type='str', required=True, aliases=['desc']),
        minutes=dict(
            type='str', required=False, default='0', aliases=['min', 'm'],
            description='Value needs to be between 0 and 59; multiple values, ranges, '
                        'steps and asterisk are supported (ex. 1,10,20,30 or 1-30).'
        ),
        hours=dict(
            type='str', required=False, default='0', aliases=['hour', 'h'],
            description='Value needs to be between 0 and 23; multiple values, ranges, '
                        'steps and asterisk are supported (ex. 1,2,8 or 0-8).'
        ),
        days=dict(
            type='str', required=False, default='*', aliases=['day', 'd'],
            description='Value needs to be between 1 and 31; multiple values, ranges, L '
                        '(last day of month), steps and asterisk are supported (ex. 1,2,8 or 1-28).'
        ),
        months=dict(
            type='str', required=False, default='*', aliases=['month', 'M'],
            description='Value needs to be between 1 and 12 or JAN to DEC, multiple values, '
                        'ranges, steps and asterisk are supported (ex. JAN,2,10 or 3-8).',
        ),
        weekdays=dict(
            type='str', required=False, default='*', aliases=['wd'],
            description='Value needs to be between 0 and 7 (Sunday to Sunday), multiple values, '
                        'ranges, steps and asterisk are supported (ex. 1,2,4 or 0-4).'
        ),
        who=dict(type='str', required=False, default='root', description='User who should run the command'),
        command=dict(
            type='str', required=False, aliases=['cmd'],
            description="One of the pre-defined commands seen in the WEB-GUI. Per example: "
                        "'automatic firmware update', 'system remote backup' or 'ipsec restart' "
                        "(always all-lowercase)"
        ),
        parameters=dict(
            type='str', required=False, aliases=['params'],
            description='Enter parameters for this job if required'
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(CronJob(m=module_input, result=result))
    return result
