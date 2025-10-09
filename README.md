# OPNsense API Client

[![Lint](https://github.com/O-X-L/opnsense-api-client/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/opnsense-api-client/actions/workflows/lint.yml)
[![Test](https://github.com/O-X-L/opnsense-api-client/actions/workflows/unit_test.yml/badge.svg)](https://github.com/O-X-L/opnsense-api-client/actions/workflows/unittest.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/oxl-opnsense-client?color=green)](https://pypi.org/project/oxl-opnsense-client/)

This is a Python3 client for interacting with the official OPNsense API.

It enables easy management and automation of OPNsense firewalls.

The base-code is a Fork of [this OPNsense Ansible-Collection](https://github.com/O-X-L/ansible-opnsense) that was refactored for use within raw Python.

This can be useful if you want to automate your Infrastructure and do not use [Ansible](https://www.ansible.com/how-ansible-works/).

An interactive CLI interface might be added later on.

----

## Install

```bash
pip install oxl-opnsense-client
```

Get to know the available modules:

* [Documentation](https://python-opnsense.oxl.app)
* [Module list](https://github.com/O-X-L/opnsense-api-client/tree/main/src/oxl_opnsense_client/plugins/modules)
* [Ansible Docs](https://ansible-opnsense.oxl.app)

----

## Contribute

The codebase of this library will be automatically synced with the upstream code of [the OPNsense Ansible-Module](https://github.com/O-X-L/ansible-opnsense)!

Thus, new features (*and feature-requests*) should be made there.

Feel free to [report issues/bugs](https://github.com/O-X-L/opnsense-api-client/issues), [take part in discussions](https://github.com/O-X-L/opnsense-api-client/discussions) and [add/extend tests](https://github.com/O-X-L/opnsense-api-client/tree/latest/src/tests).

Note: Only the [API-enabled](https://docs.opnsense.org/development/api.html) functionalities can be implemented.

----

## Usage

See also: [Ansible OPNsense-Collection Docs](https://ansible-opnsense.oxl.app/en/latest/usage/2_basic.html)

```python3
from oxl_opnsense_client import Client

with Client(
    firewall='192.168.10.20',
    port=443,  # default
    credential_file='/tmp/.opnsense.txt',
    # token='0pWN/C3tnXem6OoOp0zc9K5GUBoqBKCZ8jj8nc4LEjbFixjM0ELgEyXnb4BIqVgGNunuX0uLThblgp9Z',
    # secret='Vod5ug1kdSu3KlrYSzIZV9Ae9YFMgugCIZdIIYpefPQVhvp6KKuT7ugUIxCeKGvN6tj9uqduOzOzUlv',
) as c:
    c.test()
    # True

    ### CHECK SUPPORTED MODULES ###
    c.list_modules()
    # ['acme_account', 'acme_action', 'acme_certificate', 'acme_general', 'acme_validation', 'alias', 'alias_multi', 'alias_purge', 'bind_acl', 'bind_blocklist', 'bind_domain', 'bind_general', 'bind_record', 'bind_record_multi', 'cron', 'dhcp_controlagent', 'dhcp_general', 'dhcp_reservation', 'dhcp_subnet', 'dhcrelay_destination', 'dhcrelay_relay', 'dnsmasq_boot', 'dnsmasq_domain', 'dnsmasq_general', 'dnsmasq_host', 'dnsmasq_option', 'dnsmasq_range', 'dnsmasq_tag', 'frr_bfd_general', 'frr_bfd_neighbor', 'frr_bgp_as_path', 'frr_bgp_community_list', 'frr_bgp_general', 'frr_bgp_neighbor', 'frr_bgp_peer_group', 'frr_bgp_prefix_list', 'frr_bgp_redistribution', 'frr_bgp_route_map', 'frr_diagnostic', 'frr_general', 'frr_ospf3_general', 'frr_ospf3_interface', 'frr_ospf3_network', 'frr_ospf3_prefix_list', 'frr_ospf3_redistribution', 'frr_ospf3_route_map', 'frr_ospf_general', 'frr_ospf_interface', 'frr_ospf_network', 'frr_ospf_prefix_list', 'frr_ospf_redistribution', 'frr_ospf_route_map', 'frr_rip', 'gateway', 'group', 'hasync_general', 'hasync_service', 'ids_action', 'ids_general', 'ids_policy', 'ids_policy_rule', 'ids_rule', 'ids_ruleset', 'ids_user_rule', 'interface_bridge', 'interface_gif', 'interface_gre', 'interface_lagg', 'interface_loopback', 'interface_vip', 'interface_vlan', 'interface_vxlan', 'ipsec_auth_local', 'ipsec_auth_remote', 'ipsec_cert', 'ipsec_child', 'ipsec_connection', 'ipsec_general', 'ipsec_manual_spd', 'ipsec_pool', 'ipsec_psk', 'ipsec_vti', 'list', 'monit_alert', 'monit_service', 'monit_test', 'nat_one_to_one', 'nat_source', 'neighbor', 'nginx_general', 'nginx_upstream_server', 'openvpn_client', 'openvpn_client_override', 'openvpn_server', 'openvpn_static_key', 'openvpn_status', 'package', 'postfix_address', 'postfix_domain', 'postfix_general', 'postfix_headercheck', 'postfix_recipient', 'postfix_recipientbcc', 'postfix_sender', 'postfix_senderbcc', 'postfix_sendercanonical', 'privilege', 'raw', 'reload', 'route', 'rule', 'rule_interface_group', 'rule_multi', 'rule_purge', 'savepoint', 'service', 'shaper_pipe', 'shaper_queue', 'shaper_rule', 'snapshot', 'syslog', 'system', 'unbound_acl', 'unbound_dnsbl', 'unbound_dot', 'unbound_forward', 'unbound_general', 'unbound_host', 'unbound_host_alias', 'user', 'webproxy_acl', 'webproxy_auth', 'webproxy_cache', 'webproxy_forward', 'webproxy_general', 'webproxy_icap', 'webproxy_pac_match', 'webproxy_pac_proxy', 'webproxy_pac_rule', 'webproxy_parent', 'webproxy_remote_acl', 'webproxy_traffic', 'wireguard_general', 'wireguard_peer', 'wireguard_server', 'wireguard_show']

    ### CHECK MODULE ARGUMENTS / SPECS ###
    c.module_specs('route')
    # {'specs': {'gateway': {'type': 'str', 'required': True, 'aliases': ['gw'], 'description': 'Specify a valid existing gateway matching the networks ip protocol'}, 'network': {'type': 'str', 'required': True, 'aliases': ['nw', 'net'], 'description': 'Specify a valid network matching the gateways ip protocol'}, 'description': {'type': 'str', 'required': False, 'aliases': ['desc']}, 'match_fields': {'type': 'list', 'required': False, 'elements': 'str', 'description': "Fields that are used to match configured routes with the running config - if any of those fields are changed, the module will think it's a new route", 'choices': ['network', 'gateway', 'description'], 'default': ['network', 'gateway']}, 'reload': {'type': 'bool', 'required': False, 'default': True, 'aliases': ['apply'], 'description': 'If the running config should be reloaded/applied on change - will take some time'}, 'state': {'type': 'str', 'required': False, 'choices': ['present', 'absent'], 'default': 'present'}, 'enabled': {'type': 'bool', 'required': False, 'default': True}}}
    c.module_specs('wireguard_show', stdout=True)
    # prints in pretty-JSON

    ### CREATE ENTRY ###

    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303})
    # {'error': None, 'result': {'changed': True, 'diff': {'after': {'uuid': None, 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 5303, 'description': ''}}}}
    c.run_module('list', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': False, 'data': [{'target': '192.168.0.1', 'enabled': True, 'transport': 'udp4', 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'facility': [], 'certificate': '', 'port': 5303, 'rfc5424': False, 'description': '', 'uuid': '32b1ce94-93d0-4d20-93a2-4fff12d12a54'}]}}

    ### UPDATING ENTRY ###

    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 9941, 'match_fields': ['target']})
    # {'error': None, 'result': {'changed': True, 'diff': {'before': {'uuid': '4930e797-5111-4825-b5bb-c8e60f9d21d5', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 5304, 'description': ''}, 'after': {'uuid': '4930e797-5111-4825-b5bb-c8e60f9d21d5', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 9941, 'description': ''}}}}
    c.run_module('list', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': False, 'data': [{'target': '192.168.0.1', 'enabled': True, 'transport': 'udp4', 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'facility': [], 'certificate': '', 'port': 9941, 'rfc5424': False, 'description': '', 'uuid': '4930e797-5111-4825-b5bb-c8e60f9d21d5'}]}}

    ### DELETING ENTRY ###

    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303, 'state': 'absent', 'match_fields': ['target']})
    # {'error': None, 'result': {'changed': True, 'diff': {'before': {'uuid': '2500dadc-ce43-4e23-994e-860516b0ef45', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 5303, 'description': ''}}}}
    c.run_module('list', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': False, 'data': []}}
    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303, 'state': 'absent'})
    # {'error': None, 'result': {'changed': False, 'diff': {}}}

    ### CHECK MODE (DRY-RUN) ###

    c.run_module('syslog', check_mode=True, params={'target': '192.168.0.1', 'port': 5303})
    # {'error': None, 'result': {'changed': True, 'diff': {'before': {'uuid': '7f3aba31-07ca-4cb9-b93d-dc442a5291c7', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 5303, 'description': ''}}}}
    c.run_module('list', params={'target': 'syslog'})
    # {'error': None, 'result': {'changed': False, 'data': []}}
    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303, 'state': 'absent'})
    # {'error': None, 'result': {'changed': False, 'diff': {}}}
```

----

### Credentials

```python3
from oxl_opnsense_client import Client

# use the API credentials-file as downloaded from the WebUI
c = Client(firewall='<IP>', credential_file='/home/<YOU>/.opnsense.txt')

# use the token/key pair directly
c = Client(firewall='<IP>', token='<TOKEN>', secret='<SECRET>')
```

----

### SSL Verification

```python3
from oxl_opnsense_client import Client

# provide the path to your custom CA public-key
c = Client(
    firewall='<IP>',
    credential_file='/home/<YOU>/.opnsense.txt',
    ssl_ca_file='/home/<YOU>/ca.crt',
)

# ONLY USE FOR TESTING PURPOSES => you can disable the certificate-verification
c = Client(
    firewall='<IP>',
    credential_file='/home/<YOU>/.opnsense.txt',
    ssl_verify=False,
)
```

----

### Debug Output

This will show you the performed API calls and their JSON payload.

```python3
from oxl_opnsense_client import Client
c = Client(
    firewall='<IP>',
    credential_file='/home/<YOU>/.opnsense.txt',
    debug=True,
)

c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303})
# INFO: REQUEST: GET | URL: https://172.17.1.52/api/syslog/settings/get
# INFO: RESPONSE: '{'status_code': 200, '_request': <Request('GET', 'https://172.17.1.52/api/syslog/settings/get')>, '_num_bytes_downloaded': 123, '_elapsed': datetime.timedelta(microseconds=194859), '_content': b'{"syslog":{"general":{"enabled":"1","loglocal":"1","maxpreserve":"31","maxfilesize":""},"destinations":{"destination":[]}}}'}'
# INFO: REQUEST: POST | URL: https://172.17.1.52/api/syslog/settings/addDestination | HEADERS: '{'Content-Type': 'application/json'}' | DATA: '{"destination": {"rfc5424": 0, "enabled": 1, "hostname": "192.168.0.1", "transport": "udp4", "facility": "", "program": "", "level": "alert,crit,emerg,err,info,notice,warn", "certificate": "", "port": 5303, "description": ""}}'
# INFO: RESPONSE: '{'status_code': 200, '_request': <Request('POST', 'https://172.17.1.52/api/syslog/settings/addDestination')>, '_num_bytes_downloaded': 64, '_elapsed': datetime.timedelta(microseconds=61852), '_content': b'{"result":"saved","uuid":"ed90d52a-63ac-4d7c-a35b-4f250350f85d"}'}'
# INFO: REQUEST: POST | URL: https://172.17.1.52/api/syslog/service/reconfigure | HEADERS: '{}'
# INFO: RESPONSE: '{'status_code': 200, '_request': <Request('POST', 'https://172.17.1.52/api/syslog/service/reconfigure')>, '_num_bytes_downloaded': 15, '_elapsed': datetime.timedelta(microseconds=657156), '_content': b'{"status":"ok"}'}'
```

This information is also logged to files:

```bash
ls /tmp/opnsense_client/
# api_calls.log  syslog.log
```

The module-specific logs contain performance-profiling.
