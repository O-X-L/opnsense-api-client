from os import listdir
from pathlib import Path
from importlib import import_module
from json import dumps as json_dumps
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, gaierror

from basic.ansible import ModuleInput, AnsibleModule
from basic.exceptions import ClientFailure, ModuleFailure, ModuleHelp
from plugins.module_utils.base.api import Session
from plugins.module_utils.helper.validate import is_ip6
from plugins.module_utils.defaults.main import OPN_MOD_ARGS

_BASE_PATH = Path(__file__).parent.parent
_MODULES = [
    m.rsplit('.', 1)[0] for m in listdir(_BASE_PATH / 'plugins'  / 'modules')
    if not m.startswith('_')
]
_MODULES.sort()


class Client:
    PARAMS = [
        'firewall', 'api_port',
        'api_credential_file', 'api_token', 'api_secret',
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
        self.api_port = port
        self.api_token = token
        self.api_secret = secret
        self.api_credential_file = credential_file
        self.ssl_verify = ssl_verify
        self.ssl_ca_file = ssl_ca_file
        self.api_timeout = api_timeout
        self.api_retries = api_retries
        self.debug = debug
        self.profiling = profiling
        self.shell = shell

        self._validate_params()
        self.session = Session(module=AnsibleModule(
            argument_spec=OPN_MOD_ARGS,
            module_input=ModuleInput(client=self, params=self.params)
        ))
        self._validate_environment()

    @property
    def params(self) -> dict:
        return {k: getattr(self, k) for k in self.PARAMS}

    def _validate_params(self):
        if self.api_secret is None and self.api_credential_file is None:
            self.error('You need to either provide your API credentials (file or token + secret)!')

        if self.api_credential_file is not None:
            self.api_credential_file = Path(self.api_credential_file)
            if not self.api_credential_file.is_file():
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
                    self.params['api_port']
                )) == 0

        try:
            return _reachable(AF_INET)

        except gaierror:
            return _reachable(AF_INET6)

    def is_opnsense(self) -> bool:
        # todo: set session.url in upstream code
        fw = self.firewall
        if is_ip6(fw, strip_enclosure=False):
            fw = f"[{fw}]"

        login_page = self.session.s.get(f"https://{fw}:{self.api_port}")

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

    # pylint: disable=W0612,W0123
    def run_module(self, name: str, params: dict, check_mode: bool = False, exit_help: bool = False) -> dict:
        name = name.lower()
        if name not in _MODULES:
            raise ModuleNotFoundError('Module does not exist!')

        i = ModuleInput(
            client=self,
            params={**params, **self.params},
            check_mode=check_mode,
            exit_help=exit_help,
        )
        try:
            module = import_module(f'plugins.modules.{name}')
            result = module.run_module(i)
            return {'error': None, 'result': result}

        except (ClientFailure, ModuleFailure, ModuleNotFoundError) as e:
            if self.shell:
                raise

            return {'error': str(e), 'result': None}

    @staticmethod
    def list_modules() -> list:
        return _MODULES

    def module_specs(self, name: str, stdout: bool = False) -> (dict, None):
        try:
            self.run_module(name=name, params={}, exit_help=True)
            raise ModuleFailure()

        except ModuleHelp as e:
            specs = e.specs
            for k in OPN_MOD_ARGS:
                specs.pop(k)

            if stdout:
                print(json_dumps(specs, indent=2))
                return None

            return {'specs': specs}

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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
