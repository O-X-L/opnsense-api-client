from pathlib import Path
from sys import modules as sys_modules
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, gaierror

from .exceptions import ClientFailure, ModuleFailure
from .plugins.module_utils.base.api import Session
from .plugins.module_input import ModuleInput, empty_results

from .plugins.modules import *

_MODULES = [
    m.rsplit('.', 1)[1] for m in sys_modules if m.find('plugins.modules.') != -1
]
_BASE_PATH = Path(__file__).parent
_PLUGIN_PATH = _BASE_PATH / 'plugins'  / 'module_utils' / 'main'


class Client:
    PARAMS = [
        'firewall', 'port', 'token', 'secret', 'credential_file',
        'ssl_verify', 'ssl_ca_file', 'api_timeout', 'api_retries',
        'debug', 'profiling',
    ]
    # for ansible
    PARAM_ALIASES = {
        'api_port': 'port',
        'api_key': 'token',
        'api_secret': 'secret',
        'api_credential_file': 'credential_file',
    }

    def __init__(
            self,
            firewall: str, port: int,
            token: str = None, secret: str = None, credential_file: str = None,
            ssl_verify: bool = True, ssl_ca_file: str = None, api_timeout: float = 2.0, api_retries : int = 0,
            debug: bool = False, profiling: bool = False,
            shell: bool = True,
    ):
        self.firewall = firewall
        self.port = port
        self.token = token
        self.secret = secret
        self.credential_file = credential_file
        self.ssl_verify = ssl_verify
        self.ssl_ca_file = ssl_ca_file
        self.api_timeout = api_timeout
        self.api_retries = api_retries
        self.debug = debug
        self.profiling = profiling

        self.shell = shell

        self.params = {}
        self._build_params()
        self._validate_params()
        self.session = Session(m=self)

    def _validate_params(self):
        if self.secret is None and self.credential_file is None:
            self.error('You need to either provide your API credentials (file or token + secret)!')

        if not self.reachable():
            self.error('The firewall is unreachable!')

        if self.credential_file is not None:
            self.credential_file = Path(self.credential_file)
            if not self.credential_file.is_file():
                self.error('The provided Credentials-File does not exist!')

        if self.ssl_ca_file is not None:
            self.ssl_ca_file = Path(self.ssl_ca_file)
            if not self.ssl_ca_file.is_file():
                self.error('The provided CA-File does not exist!')

    def test(self) -> bool:
        t = self.reachable()
        if t:
            print('OK')
            return t

        print('UNREACHABLE')
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

    def _build_params(self):
        d = {k: getattr(self, k) for k in self.PARAMS}
        da = {k: d[v] for k, v in self.PARAM_ALIASES.items()}
        self.params = {**d, **da}

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

    # legacy name for ansible-compatibility
    def fail_json(self, msg: str):
        self.error(msg)

    def warn(self, msg: str):
        if self.shell:
            print(f"\x1b[1;33mWARN: {msg}\x1b[0m\n")

        else:
            print(f"WARN: {msg}")

    @staticmethod
    def info(msg: str):
        print(f"INFO: {msg}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
