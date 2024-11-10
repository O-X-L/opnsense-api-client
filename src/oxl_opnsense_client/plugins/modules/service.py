from ..module_input import validate_input, ModuleInput, valid_results

# c = api-module, m = custom action-mapping, a = limited actions
SERVICES = {
    # core api
    'captive_portal': {'c': 'captiveportal', 'a': ['reload']},
    'cron': {'a': ['reload']},
    'ipsec_legacy': {'c': 'legacy_subsystem', 'a': ['reload'], 'm': {'reload': 'applyConfig'}},
    'ipsec': {}, 'monit': {}, 'syslog': {},
    'shaper': {
        'c': 'trafficshaper', 'a': ['reload', 'status', 'restart'],
        'm': {'restart': 'flushreload', 'status': 'statistics'}
    },
    'openvpn': {
        'c': 'openvpn', 'a': ['stop', 'status', 'start', 'reload', 'restart'],
        'm': {
            'start': 'startService', 'reload': 'reconfigure', 'restart': 'restartService',
            'status': 'searchSessions', 'stop': 'stopService',
        },
    },
    #   note: these would support more actions:
    'ids': {}, 'proxy': {}, 'unbound': {},
    # plugins
    'ftp_proxy': {'c': 'ftpproxy'},
    'iperf': {'a': ['reload', 'status', 'start', 'restart']},
    'mdns_repeater': {'c': 'mdnsrepeater', 'a': ['stop', 'status', 'start', 'restart']},
    'munin_node': {'c': 'muninnode'},
    'node_exporter': {'c': 'nodeexporter'},
    'puppet_agent': {'c': 'puppetagent'},
    'qemu_guest_agent': {'c': 'qemuguestagent'},
    'frr': {'c': 'quagga'},
    'radsec_proxy': {'c': 'radsecproxy'},
    'zabbix_agent': {'c': 'zabbixagent'},
    'zabbix_proxy': {'c': 'zabbixproxy'},
    'apcupsd': {}, 'bind': {}, 'chrony': {}, 'cicap': {}, 'collectd': {},
    'dyndns': {}, 'fetchmail': {}, 'freeradius': {}, 'haproxy': {}, 'maltrail': {},
    'netdata': {}, 'netsnmp': {}, 'nrpe': {}, 'nut': {}, 'openconnect': {}, 'proxysso': {},
    'rspamd': {}, 'shadowsocks': {}, 'softether': {}, 'sslh': {}, 'stunnel': {}, 'tayga': {},
    'telegraf': {}, 'tftp': {}, 'tinc': {}, 'wireguard': {},
    #   note: these would support more actions:
    'acme_client': {'c': 'acmeclient'},
    'crowdsec': {'a': ['reload', 'status']},
    'dns_crypt_proxy': {'c': 'dnscryptproxy'},
    'udp_broadcast_relay': {'c': 'udpbroadcastrelay'},
    'clamav': {}, 'hwprobe': {}, 'lldpd': {}, 'nginx': {}, 'ntopng': {}, 'postfix': {}, 'redis': {},
    'relayd': {}, 'siproxd': {}, 'vnstat': {}, 'tor': {},
}

ACTION_MAPPING = {'reload': 'reconfigure'}
API_CONTROLLER = 'service'


# pylint: disable=R0915
def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    m = module_input
    result = valid_results(result)

    service_choices = list(SERVICES.keys())
    service_choices.sort()

    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['service', 'svc', 'target', 'n'],
            choices=service_choices,
            description='What service to interact with'
        ),
        action=dict(
            type='str', required=True, aliases=['do', 'a'],
            choices=['reload', 'restart', 'start', 'status', 'stop'],
            description='What action to execute. Some services may not support all of these actions - '
                        'the module will inform you in that case'
        ),
    )

    validate_input(i=module_input, definition=module_args)

    name = m.params['name']
    action = m.params['action']
    service = SERVICES[name]

    if 'a' in service and action not in service['a']:
        m.fail(
            f"Service '{name}' does not support the "
            f"provided action '{action}'! "
            f"Supported ones are: {service['a']}"
        )

    # translate actions to api-commands
    # pylint: disable=R1715
    if 'm' in service and action in service['m']:
        action = service['m'][action]

    elif action in ACTION_MAPPING:
        action = ACTION_MAPPING[action]

    result['executed'] = action

    # get api-module
    if 'c' in service:
        api_module = service['c']

    else:
        api_module = name

    # pull status or execute action
    if m.params['action'] == 'status':
        info = m.c.session.get(
            cnf={
                'module': api_module,
                'controller': API_CONTROLLER,
                'command': action,
            }
        )

        if 'response' in info:
            info = info['response']

            if isinstance(info, str):
                info = info.strip()

        result['data'] = info

    else:
        result['changed'] = True

        if not m.check_mode:
            m.c.session.post(
                cnf={
                    'module': api_module,
                    'controller': API_CONTROLLER,
                    'command': action,
                }
            )

    return result
