

def test_client_creation():
    from oxl_opnsense_client import Client

    c = Client(
        firewall='www.google.com',
        token='<TOKEN>',
        secret='<SECRET>',
    )
    del c

    with Client(
        firewall='www.google.com',
        token='<TOKEN>',
        secret='<SECRET>',
    ) as _:
        pass


def test_client_unreachable():
    from oxl_opnsense_client import Client
    from oxl_opnsense_client.exceptions import ClientFailure

    try:
        with Client(
            firewall='192.168.10.20',
            port=13498,
            token='<TOKEN>',
            secret='<SECRET>',
        ) as _:
            assert False

    except ClientFailure as e:
        assert str(e).find('unreachable') != -1


def test_bad_creds():
    from oxl_opnsense_client import Client
    from oxl_opnsense_client.exceptions import ClientFailure

    try:
        with Client(
            firewall='192.168.10.20',
        ) as _:
            assert False

    except ClientFailure as e:
        assert str(e).find('API credentials') != -1

    try:
        with Client(
            firewall='192.168.10.20',
            credential_file='/tmp/daösfslekföslekföske'
        ) as _:
            assert False

    except ClientFailure as e:
        assert str(e).find('does not exist') != -1
