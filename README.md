# OPNSense API Client

[![Lint](https://github.com/O-X-L/opnsense-api-client/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/opnsense-api-client/actions/workflows/lint.yml)
[![Test](https://github.com/O-X-L/opnsense-api-client/actions/workflows/unittest.yml/badge.svg)](https://github.com/O-X-L/opnsense-api-client/actions/workflows/unittest.yml)

This is a Python3 client for interacting with the official OPNSense API.

It enables simple management and automation of OPNSense firewalls. An interactive CLI interface might be added later on.

The base-code is a Fork of this [OPNSense Ansible-Collection](https://github.com/ansibleguy/collection_opnsense) that was refactored for use within raw Python.

This can be useful if you want to automate your Infrastructure and do not use [Ansible](https://www.ansible.com/how-ansible-works/).

**WARNING**: This project is still in early development! The forked code is pretty much stable, but the refactor may not yet be.

----

## Install

```bash
pip install oxl-opnsense-client
```

Get to know the available modules:

* [Module list](https://github.com/O-X-L/opnsense-api-client/tree/main/src/oxl_opnsense_client/plugins/modules)
* [Ansible Docs](https://opnsense.ansibleguy.net)

----

## Contribute

Feel free to [report issues/bugs](https://github.com/O-X-L/opnsense-api-client/issues), [take part in discussions](https://github.com/O-X-L/opnsense-api-client/discussions), [add/extend tests](https://github.com/O-X-L/opnsense-api-client/tree/latest/src/tests) and [provide PRs to enhance or extend the codebase](https://github.com/O-X-L/opnsense-api-client/pulls).

Note: Only the [API-enabled](https://docs.opnsense.org/development/api.html) functionalities can be implemented.

----

## Advertisement

* Need **professional support** for IT-Automation or OPNSense? Contact us:

  E-Mail: [contact@oxl.at](mailto:contact@oxl.at)

  Tel: [+43 3115 40 900 0](tel:+433115409000)

  Web: [EN](https://www.o-x-l.com) | [DE](https://www.oxl.at)

  Language: German or English

----

## Usage

See also: [Ansible OPNSense-Collection Docs](https://opnsense.ansibleguy.net/en/latest/usage/2_basic.html)

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

    ### CREATE / REMOVE ENTRIES ###
    
    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303})
    # {'error': None, 'result': {'changed': True, 'diff': {'after': {'uuid': None, 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 5303, 'description': ''}}}}
    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303, 'state': 'absent'})
    # {'error': None, 'result': {'changed': True, 'diff': {'before': {'uuid': '2500dadc-ce43-4e23-994e-860516b0ef45', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 5303, 'description': ''}}}}
    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303, 'state': 'absent'})
    # {'error': None, 'result': {'changed': False, 'diff': {}}}

    ### CHECK MODE (DRY-RUN) ###
    
    c.run_module('syslog', check_mode=True, params={'target': '192.168.0.1', 'port': 5303})
    # {'error': None, 'result': {'changed': True, 'diff': {'before': {'uuid': '7f3aba31-07ca-4cb9-b93d-dc442a5291c7', 'rfc5424': False, 'enabled': True, 'target': '192.168.0.1', 'transport': 'udp4', 'facility': [], 'program': [], 'level': ['alert', 'crit', 'emerg', 'err', 'info', 'notice', 'warn'], 'certificate': '', 'port': 5303, 'description': ''}}}}
    c.run_module('syslog', params={'target': '192.168.0.1', 'port': 5303, 'state': 'absent'})
    # {'error': None, 'result': {'changed': False, 'diff': {}}}
```


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
