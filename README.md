# OPNSense API Client

This is a client for interacting with the official OPNSense API.

This can be useful if you want to automate your Infrastructure and do not use [Ansible](https://www.ansible.com/how-ansible-works/).

The base-code is a Fork of this [OPNSense Ansible-Collection](https://github.com/ansibleguy/collection_opnsense) that was refactored for use within raw Python.

**WARNING**: This project is still in early development! The forked code is pretty much stable, but the refactor may not yet be.

----

## Install

```bash
pip install oxl-opnsense-client
```

```python3cc
from oxl_opnsense_client import Client

with Client(
    firewall='192.168.10.20',
    port=443,  # default
    credential_file='/tmp/.opnsense.txt',
    # token='0pWN/C3tnXem6OoOp0zc9K5GUBoqBKCZ8jj8nc4LEjbFixjM0ELgEyXnb4BIqVgGNunuX0uLThblgp9Z',
    # secret='Vod5ug1kdSu3KlrYSzIZV9Ae9YFMgugCIZdIIYpefPQVhvp6KKuT7ugUIxCeKGvN6tj9uqduOzOzUlv',
) as client:
    client.test()
    > OK
```

----

## Contribute

Feel free to [report issues/bugs](https://github.com/O-X-L/opnsense-api-client/issues), [take part in discussions](https://github.com/O-X-L/opnsense-api-client/discussions) and [provide PRs to enhance or extend the codebase](https://github.com/O-X-L/opnsense-api-client/pulls).

----

## Usage

See also: [Ansible OPNSense-Collection Docs](https://opnsense.ansibleguy.net/en/latest/usage/2_basic.html)

### Credentials

```python3
from oxl_opnsense_client import Client

# use the API credentials-file as downloaded from the WebUI
c = Client(firewall='<IP>', credential_file='/home/<YOU>/.opnsense.txt')

# use the token/key pair directly
c = Client(firewall='<IP>', token='<TOKEN>', secret='<SECRET>')
```

----

### Debug Output

This will show you the performed API calls and their JSON payload.

```python3
from oxl_opnsense_client import Client
c = Client(firewall='<IP>', credential_file='/home/<YOU>/.opnsense.txt', debug=True)

# Example output:
# INFO: REQUEST: GET | URL: https://<IP>/api/syslog/settings/get
# INFO: RESPONSE: '{'status_code': 200, '_request': <Request('GET', 'https://<IP>/api/syslog/settings/get')>, '_num_bytes_downloaded': 123, '_elapsed': datetime.timedelta(microseconds=191725), '_content': b'{"syslog":{"general":{"enabled":"1","loglocal":"1","maxpreserve":"31","maxfilesize":""},"destinations":{"destination":[]}}}'}'
# INFO: REQUEST: POST | URL: https://<IP>/api/syslog/settings/addDestination | HEADERS: '{'Content-Type': 'application/json'}' | DATA: '{"destination": {"rfc5424": 0, "enabled": 1, "hostname": "192.168.0.1", "transport": "udp4", "facility": "", "program": "", "level": "alert,crit,emerg,err,info,notice,warn", "certificate": "None", "port": 5303, "description": "None"}}'
# INFO: RESPONSE: '{'status_code': 200, '_request': <Request('POST', 'https://<IP>/api/syslog/settings/addDestination')>, '_num_bytes_downloaded': 111, '_elapsed': datetime.timedelta(microseconds=78827), '_content': b'{"result":"failed","validations":{"destination.certificate":"Please select a valid certificate from the list"}}'}'
```

----

### SSL Verification

```python3
from oxl_opnsense_client import Client

# provide the path to your custom CA public-key
c = Client(firewall='<IP>', credential_file='/home/<YOU>/.opnsense.txt', ssl_ca_file='/home/<YOU>/ca.crt')

# ONLY USE FOR TESTING PURPOSES => you can disable the certificate-verification
c = Client(firewall='<IP>', credential_file='/home/<YOU>/.opnsense.txt', ssl_verify=False)
```
