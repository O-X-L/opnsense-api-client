from pathlib import Path
from sys import modules as sys_modules
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, gaierror

from .exceptions import ClientFailure, ModuleFailure
from .plugins.module_utils.base.api import Session
from .plugins.module_input import ModuleInput, empty_results

# pylint: disable=W0401,W0614
from .plugins.modules import *

_MODULES = [
    m.rsplit('.', 1)[1] for m in sys_modules if m.find('plugins.modules.') != -1
]
_BASE_PATH = Path(__file__).parent
_PLUGIN_PATH = _BASE_PATH / 'plugins'  / 'module_utils' / 'main'


class Client:
    PARAMS = [
        'firewall', 'port',
        'ssl_verify', 'ssl_ca_file', 'api_timeout', 'api_retries',
        'debug', 'profiling',
    ]

    # pylint: disable=R0913,R0917
    def __init__(
            self,
            firewall: str, token: str = None, secret: str = None, credential_file: str = None, port: int = 443,
            ssl_verify: bool = True, ssl_ca_file: str = None, api_timeout: float = 2.0, api_retries : int = 0,
            debug: bool = False, profiling: bool = False,
            shell: bool = True,
    ):
        self.firewall = firewall
        self.port = port
        self.credential_file = credential_file
        self.ssl_verify = ssl_verify
        self.ssl_ca_file = ssl_ca_file
        self.api_timeout = api_timeout
        self.api_retries = api_retries
        self.debug = debug
        self.profiling = profiling
        self.shell = shell

        self._api_token = token
        self._api_secret = secret
        self._load_credentials_from_file()

        self._validate_params()
        self.session = Session(m=self, token=self._api_token, secret=self._api_secret)
        self._validate_environment()

    def _validate_params(self):
        if self._api_secret is None and self.credential_file is None:
            self.error('You need to either provide your API credentials (file or token + secret)!')

        if self.credential_file is not None:
            self.credential_file = Path(self.credential_file)
            if not self.credential_file.is_file():
                self.error('The provided Credentials-File does not exist!')

        if self.ssl_ca_file is not None:
            self.ssl_ca_file = Path(self.ssl_ca_file)
            if not self.ssl_ca_file.is_file():
                self.error('The provided CA-File does not exist!')

    def _validate_environment(self):
        if not self.reachable():
            self.error('The firewall is unreachable!')

        if not self.is_opnsense():
            self.warn('The target may not be an OPNsense!')

    def test(self) -> bool:
        t = self.reachable()
        if t:
            t = self.is_opnsense()

        if t:
            t = self.correct_credentials()

        if self.shell:
            print('OK' if t else 'UNREACHABLE')

        return t

    def reachable(self) -> bool:
        def _reachable(address_family: int) -> bool:
            with socket(address_family, SOCK_STREAM) as s:
                s.settimeout(self.api_timeout)
                return s.connect_ex((
                    self.params['firewall'],
                    self.params['port']
                )) == 0

        try:
            return _reachable(AF_INET)

        except gaierror:
            return _reachable(AF_INET6)

    def is_opnsense(self) -> bool:
        login_page = self.session.s.get(self.session.url)

        if login_page.status_code != 200:
            return False

        return login_page.content.find(b'OPNsense') != -1

    def correct_credentials(self) -> (bool, None):
        if not self.reachable():
            return None

        try:
            self.run_module('meta_list', params={'target': 'interface_vip'})
            return True

        except ClientFailure:
            return False

    @property
    def params(self) -> dict:
        return {k: getattr(self, k) for k in self.PARAMS}

    # pylint: disable=W0612,W0123
    def run_module(self, name: str, params: dict, check_mode: bool = False) -> dict:
        name = name.lower()
        if name not in _MODULES:
            raise ModuleNotFoundError('Module does not exist!')

        i = ModuleInput(client=self, params=params, check_mode=check_mode)
        r = empty_results()
        try:
            eval(f'{name}(i, r)')
            return {'error': None, 'result': r}

        except (ClientFailure, ModuleFailure) as e:
            if self.shell:
                raise

            return {'error': str(e), 'result': r}


    def error(self, msg: str):
        if self.shell:
            raise ClientFailure(f"\x1b[1;31mERROR: {msg}\x1b[0m\n")

        raise ClientFailure(f"ERROR: {msg}")

    def fail(self, msg: str):
        self.error(msg)

    def warn(self, msg: str):
        if self.shell:
            print(f"\x1b[1;33mWARN: {msg}\x1b[0m\n")

        else:
            print(f"WARN: {msg}")

    @staticmethod
    def info(msg: str):
        print(f"INFO: {msg}")

    def _load_credentials_from_file(self) -> None:
        if self.credential_file is None:
            return

        cred_file_info = Path(self.credential_file)

        if cred_file_info.is_file():
            cred_file_mode = oct(cred_file_info.stat().st_mode)[-3:]

            if int(cred_file_mode[2]) != 0:
                self.warn(
                    f"Provided 'credential_file' at path "
                    f"'{self.credential_file}' is world-readable "
                    f"(mode {cred_file_mode})!"
                )

            with open(self.credential_file, 'r', encoding='utf-8') as file:
                config = {}

                for line in file.readlines():
                    try:
                        key, value = line.split('=', 1)
                        config[key] = value.strip()

                    except ValueError:
                        pass

                if 'key' not in config or 'secret' not in config:
                    self.fail(
                        f"Credential file '{self.credential_file}' "
                        'could not be parsed!'
                    )

                self._api_token = config['key']
                self._api_secret = config['secret']

        else:
            self.fail(
                f"Provided 'credential_file' at path "
                f"'{self.credential_file}' does not exist!"
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
