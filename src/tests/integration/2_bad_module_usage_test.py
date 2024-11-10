from tests.integration import config
from oxl_opnsense_client.exceptions import ModuleFailure


def test_nonexisting_module():
    from oxl_opnsense_client import Client

    with Client(
        firewall=config.FIREWALL,
        port=config.PORT,
        credential_file=config.CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        try:
            c.run_module('XXX', params={'a': 'b'})
            assert False

        except ModuleNotFoundError as e:
            assert str(e).find('Module does not exist') != -1


def test_input_validation():
    from oxl_opnsense_client import Client

    with Client(
        firewall=config.FIREWALL,
        port=config.PORT,
        credential_file=config.CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        try:
            c.run_module('syslog', params={})
            assert False

        except ModuleFailure as e:
            assert str(e).find('No parameters') != -1

        try:
            c.run_module('syslog', params={'target': '192.168.0.1', 'port': 'abc'})
            assert False

        except ModuleFailure as e:
            assert str(e).find('invalid type') != -1

        try:
            c.run_module('syslog', params={'port': 80})
            assert False

        except ModuleFailure as e:
            assert str(e).find('required parameter') != -1

        try:
            c.run_module('syslog', params={'target': '192.168.0.1', 'level': ['alert', 'XXX']})
            assert False

        except ModuleFailure as e:
            assert str(e).find('invalid value') != -1
