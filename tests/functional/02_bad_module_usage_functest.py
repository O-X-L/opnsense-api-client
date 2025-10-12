from test_config import *

from basic.exceptions import ClientFailure

# todo: move to unit-tests via mocking


def test_nonexisting_module():
    from basic.client import Client

    with Client(
        firewall=FIREWALL,
        port=PORT,
        credential_file=CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        try:
            c.run_module('XXX', params={'a': 'b'})
            assert False

        except ModuleNotFoundError as e:
            assert str(e).find('Module does not exist') != -1


def test_input_validation():
    from basic.client import Client

    with Client(
        firewall=FIREWALL,
        port=PORT,
        credential_file=CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        try:
            c.run_module('syslog', params={})
            assert False

        except ClientFailure as e:
            assert str(e).find('missing required arguments') != -1

        try:
            c.run_module('syslog', params={'target': '192.168.0.1', 'port': 'abc'})
            assert False

        except ClientFailure as e:
            assert str(e).find('unable to convert to int') != -1

        try:
            c.run_module('syslog', params={'port': 80})
            assert False

        except ClientFailure as e:
            assert str(e).find('missing required arguments') != -1

        try:
            c.run_module('syslog', params={'target': '192.168.0.1', 'level': ['alert', 'XXX']})
            assert False

        except ClientFailure as e:
            assert str(e).find('value of level must be one or more of') != -1
