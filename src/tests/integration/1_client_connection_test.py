from httpx import ConnectError

from tests.integration import config


def test_environment_checks():
    from oxl_opnsense_client import Client

    with Client(
        firewall=config.FIREWALL,
        port=config.PORT,
        credential_file=config.CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        assert c.reachable()
        assert c.is_opnsense()


def test_credentials():
    from oxl_opnsense_client import Client

    with Client(
        firewall=config.FIREWALL,
        port=config.PORT,
        credential_file=config.CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        assert c.reachable()
        assert c.is_opnsense()
        assert c.correct_credentials()

    with Client(
        firewall=config.FIREWALL,
        port=config.PORT,
        token=config.TOKEN,
        secret=config.SECRET,
        ssl_verify=False,
    ) as c:
        assert c.reachable()
        assert c.is_opnsense()
        assert c.correct_credentials()


def test_check():
    from oxl_opnsense_client import Client

    with Client(
        firewall=config.FIREWALL,
        port=config.PORT,
        credential_file=config.CREDENTIAL_FILE,
        ssl_verify=False,
    ) as c:
        assert c.test()


def test_ssl_verification():
    from oxl_opnsense_client import Client

    try:
        with Client(
            firewall=config.FIREWALL,
            port=config.PORT,
            credential_file=config.CREDENTIAL_FILE,
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
