from test_config import *

TEST_ALIAS = 'API_CLI_TEST_1'
# todo: move to unit-tests via mocking

def test_alias_cleanup():
    from basic.client import Client

    with Client(
        firewall=FIREWALL,
        port=PORT,
        credential_file=CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        c.run_module('alias', params={
            'name': TEST_ALIAS, 'state': 'absent',
        })


def test_alias_create():
    from basic.client import Client

    with Client(
        firewall=FIREWALL,
        port=PORT,
        credential_file=CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        d = c.run_module('list', params={'target': 'alias'})
        assert len(d['result']['data']) == 0

        d = c.run_module('alias', params={
            'name': TEST_ALIAS, 'type': 'network', 'content': ['10.0.0.0/24'],
        })
        assert d['result']['changed']
        assert d['result']['diff']['before'] is None
        assert d['result']['diff']['after'] is not None

        d = c.run_module('list', params={'target': 'alias'})
        assert len(d['result']['data']) == 1
        assert d['result']['data'][0]['name'] == TEST_ALIAS


def test_alias_change():
    from basic.client import Client

    with Client(
        firewall=FIREWALL,
        port=PORT,
        credential_file=CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        d = c.run_module('list', params={'target': 'alias'})
        assert len(d['result']['data']) == 1

        d = c.run_module('alias', params={
            'name': TEST_ALIAS, 'type': 'network', 'content': ['10.0.100.0/24'],
        })
        assert d['result']['changed']
        assert d['result']['diff']['before']['content'] == ['10.0.0.0/24']
        assert d['result']['diff']['after']['content'] == ['10.0.100.0/24']

        d = c.run_module('list', params={'target': 'alias'})
        assert len(d['result']['data']) == 1


def test_alias_delete():
    from basic.client import Client

    with Client(
        firewall=FIREWALL,
        port=PORT,
        credential_file=CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        d = c.run_module('list', params={'target': 'alias'})
        assert len(d['result']['data']) == 1

        c.run_module('alias', params={
            'name': TEST_ALIAS, 'state': 'absent',
        })

        d = c.run_module('list', params={'target': 'alias'})
        assert len(d['result']['data']) == 0
