from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, gaierror
from time import time, sleep
from datetime import datetime


from ..base.api import Session, HTTPX_EXCEPTIONS
from ..defaults.main import CONNECTION_TEST_TIMEOUT


def _opn_reachable_ipv(m, address_family: int) -> bool:
    with socket(address_family, SOCK_STREAM) as s:
        s.settimeout(CONNECTION_TEST_TIMEOUT)
        return s.connect_ex((
            m.params['firewall'],
            m.params['port']
        )) == 0


def _opn_reachable(m) -> bool:
    try:
        return _opn_reachable_ipv(m, AF_INET)

    except gaierror:
        return _opn_reachable_ipv(m, AF_INET6)


def _wait_msg(m, msg: str):
    m.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {msg}")


def wait_for_response(m) -> bool:
    timeout = time() + m.params['wait_timeout']

    _wait_msg(m, 'Waiting for services to stop..')
    sleep(10)

    while time() < timeout:
        poll_interval_start = time()

        if _opn_reachable(m=m):
            _wait_msg(m, 'Got response!')
            return True

        _wait_msg(m, 'Waiting for response..')
        poll_interval_elapsed = time() - poll_interval_start
        if poll_interval_elapsed < m.params['poll_interval']:
            sleep(m.params['poll_interval'] - poll_interval_elapsed)

    raise TimeoutError


def get_upgrade_status(s: Session) -> dict:
    return s.get({
        'command': 'upgradestatus',
        'module': 'core',
        'controller': 'firmware',
    })


def wait_for_update(m, s: Session) -> bool:
    timeout = time() + m.params['wait_timeout']

    if m.params['action'] == 'upgrade':
        _wait_msg(m, 'Waiting for download & upgrade to finish..')

    else:
        _wait_msg(m, 'Waiting for update to finish..')

    sleep(2)

    while time() < timeout:
        poll_interval_start = time()

        try:
            result = get_upgrade_status(s)
            status = result['status']

            _wait_msg(m, f"Got response: {status}")

            if status == 'error' and 'log' in result:
                _wait_msg(m, f"Got error: {result['log']}")
                return False

            if status == 'done':
                _wait_msg(m, f"Got result: {result['log']}")
                return True

        except (HTTPX_EXCEPTIONS, ConnectionError, TimeoutError):
            # not reachable while rebooting
            _wait_msg(m, 'Waiting for response..')

        poll_interval_elapsed = time() - poll_interval_start
        if poll_interval_elapsed < m.params['poll_interval']:
            sleep(m.params['poll_interval'] - poll_interval_elapsed)

    raise TimeoutError
