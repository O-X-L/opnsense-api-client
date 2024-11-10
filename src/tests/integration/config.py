from os import environ

try:
    FIREWALL = environ['FIREWALL']
    PORT = environ['PORT'] if 'PORT' in environ else 443
    TOKEN = environ['TOKEN']
    SECRET = environ['SECRET']
    CREDENTIAL_FILE = environ['CREDENTIAL_FILE']
    SSL_CA_FILE = environ['SSL_CA_FILE']

except KeyError:
    raise EnvironmentError(
        'You need to define these env-vars: '
        'FIREWALL, PORT, TOKEN, SECRET, CREDENTIAL_FILE, SSL_CA_FILE'
    )
