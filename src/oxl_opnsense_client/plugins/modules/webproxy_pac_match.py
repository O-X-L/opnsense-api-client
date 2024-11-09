from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.webproxy_pac_match import Match

MONTH_MAPPING = {
    1: 'JAN',
    2: 'FEB',
    3: 'MAR',
    4: 'APR',
    5: 'MAY',
    6: 'JUN',
    7: 'JUL',
    8: 'AUG',
    9: 'SEP',
    10: 'OCT',
    11: 'NOV',
    12: 'DEC',
}

WEEKDAY_MAPPING = {
    1: 'MON',
    2: 'TUE',
    3: 'WED',
    4: 'THU',
    5: 'FRI',
    6: 'SAT',
    7: 'SUN',
}


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    module_args = dict(
        name=dict(
            type='str', required=True, description='Unique name for the match',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        negate=dict(
            type='bool', required=False, default=False,
            description='Negate this match. '
                        'For example you can match if a host is not inside a network'
        ),
        type=dict(
            type='str', required=False, default='url_matches',
            choices=[
                'url_matches', 'hostname_matches', 'dns_domain_is', 'destination_in_net',
                'my_ip_in_net', 'plain_hostname', 'is_resolvable', 'dns_domain_levels',
                'weekday_range', 'date_range', 'time_range',
            ],
            description='The type of the match. Depending on the match, you will need '
                        'different arguments',
        ),
        hostname=dict(
            type='str', required=False,
            description='A hostname pattern like *.opnsense.org',
        ),
        url=dict(
            type='str', required=False,
            description='A URL pattern like forum.opnsense.org/index*',
        ),
        network=dict(
            type='str', required=False,
            description='The network address to match in CIDR notation for example '
                        'like 127.0.0.1/8 or ::1/128',
        ),
        domain_level_from=dict(
            type='int', required=False, default=0, aliases=['domain_from'],
            description='The minimum amount of dots in the domain name',
        ),
        domain_level_to=dict(
            type='int', required=False, default=0, aliases=['domain_to'],
            description='The maximum amount of dots in the domain name',
        ),
        hour_from=dict(
            type='int', required=False, default=0, aliases=['time_from'],
            description='Start hour for match-period',
        ),
        hour_to=dict(
            type='int', required=False, default=0, aliases=['time_to'],
            description='End hour for match-period',
        ),
        month_from=dict(
            type='int', required=False, default=1, aliases=['date_from'],
            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            description='Start month for match-period',
        ),
        month_to=dict(
            type='int', required=False, default=1, aliases=['date_to'],
            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            description='End month for match-period',
        ),
        weekday_from=dict(
            type='int', required=False, default=1, aliases=['day_from'],
            choices=[1, 2, 3, 4, 5, 6, 7],
            description='Start weekday for match-period. 1 = monday, 7 = sunday',
        ),
        weekday_to=dict(
            type='int', required=False, default=1, aliases=['day_to'],
            choices=[1, 2, 3, 4, 5, 6, 7],
            description='End weekday for match-period. 1 = monday, 7 = sunday',
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)

    for day_field in ['weekday_from', 'weekday_to']:
        m.params[day_field] = WEEKDAY_MAPPING[m.params[day_field]]

    for month_field in ['month_from', 'month_to']:
        m.params[month_field] = MONTH_MAPPING[m.params[month_field]]


    module_wrapper(Match(m=module_input, result=result))
    return result
