from os import environ
from pathlib import Path


def _read_token_secret(file: str) -> tuple:
    if not Path(file).is_file():
        raise FileNotFoundError(f'Credential file not found or readable: {file}')

    with open(file, 'r', encoding='utf-8') as f:
        token = f.readline().split('=', 1)[1].strip()
        secret = f.readline().split('=', 1)[1].strip()

    return token, secret


try:
    FIREWALL = environ['TEST_FIREWALL']
    PORT = environ.get('TEST_PORT', 443)
    CREDENTIAL_FILE = environ['TEST_API_CREDS']
    TOKEN, SECRET = _read_token_secret(CREDENTIAL_FILE)

except KeyError:
    raise EnvironmentError(
        'You need to define these env-vars: '
        'TEST_FIREWALL, TEST_API_CREDS'
    )
