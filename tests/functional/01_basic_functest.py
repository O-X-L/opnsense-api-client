from httpx import ConnectError

from test_config import *


def test_environment_checks():
    from basic.client import Client

    with Client(
        firewall=FIREWALL,
        port=PORT,
        credential_file=CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        assert c.reachable()
        assert c.is_opnsense()


def test_credentials():
    from basic.client import Client

    with Client(
        firewall=FIREWALL,
        port=PORT,
        credential_file=CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        assert c.reachable()
        assert c.is_opnsense()
        assert c.correct_credentials()

    with Client(
        firewall=FIREWALL,
        port=PORT,
        token=TOKEN,
        secret=SECRET,
        ssl_verify=False,
    ) as c:
        assert c.reachable()
        assert c.is_opnsense()
        assert c.correct_credentials()


def test_check():
    from basic.client import Client

    with Client(
        firewall=FIREWALL,
        port=PORT,
        credential_file=CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        assert c.test()


def test_ssl_verification():
    from basic.client import Client

    try:
        with Client(
            firewall=FIREWALL,
            port=PORT,
            credential_file=CREDENTIAL_FILE,
        ) as _:
            assert False

    except ConnectError as e:
        assert str(e).find('CERTIFICATE_VERIFY_FAILED') != -1

    # todo: ca-signed cert with correct SAN
    # try:
    #     with Client(
    #         firewall=config.FIREWALL,
    #         port=config.PORT,
    #         credential_file=config.CREDENTIAL_FILE,
    #         ssl_ca_file=config.SSL_CA_FILE,
    #     ) as _:
    #         assert True
    #
    # except ConnectError as e:
    #     assert False
