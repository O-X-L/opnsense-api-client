from socket import setdefaulttimeout

import httpx

from ..helper.api import \
    check_host, ssl_verification, check_response, get_params_path, debug_api, api_pretty_exception
from ..helper.main import is_ip6

DEFAULT_TIMEOUT = 20.0
HTTPX_EXCEPTIONS = (
    httpx.ConnectTimeout, httpx.ConnectError, httpx.ReadTimeout, httpx.WriteTimeout,
    httpx.TimeoutException, httpx.PoolTimeout,
)


class Session:
    def __init__(self, m, token: str, secret: str, timeout: float = DEFAULT_TIMEOUT):
        self.m = m
        self.timeout = timeout
        self.url = ''
        self.s = self._start(timeout, token=token, secret=secret)

    def _start(self, timeout: float, token: str, secret: str) -> httpx.Client:
        check_host(m=self.m)

        if 'api_timeout' in self.m.params and self.m.params['api_timeout'] is not None:
            timeout = self.m.params['api_timeout']

        setdefaulttimeout(timeout)

        fw = self.m.params['firewall']
        if is_ip6(fw, strip_enclosure=False):
            fw = f"[{fw}]"

        self.url = f"https://{fw}:{self.m.params['port']}"

        return httpx.Client(
            base_url=f"{self.url}/api",
            auth=(token, secret),
            timeout=httpx.Timeout(timeout=timeout, connect=2.0),
            transport=httpx.HTTPTransport(
                verify=ssl_verification(m=self.m),
                retries=self.m.params['api_retries'],
            ),
        )

    def get(self, cnf: dict, timeout: float = DEFAULT_TIMEOUT) -> dict:
        params_path = get_params_path(cnf=cnf)
        call_url = f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

        debug_api(
            m=self.m,
            method='GET',
            url=f'{self.s.base_url}{call_url}',
        )

        try:
            response = check_response(
                m=self.m,
                cnf=cnf,
                response=self.s.get(url=call_url, timeout=timeout)
            )

        except HTTPX_EXCEPTIONS as error:
            api_pretty_exception(
                m=self.m, method='GET', error=error,
                url=f'{self.s.base_url}{call_url}',
            )
            raise

        return response

    def post(self, cnf: dict, headers: dict = None, timeout: float = DEFAULT_TIMEOUT) -> dict:
        if headers is None:
            headers = {}

        data = None

        if 'data' in cnf and cnf['data'] is not None and len(cnf['data']) > 0:
            headers['Content-Type'] = 'application/json'
            data = cnf['data']

        params_path = get_params_path(cnf=cnf)
        call_url = f"{cnf['module']}/{cnf['controller']}/{cnf['command']}{params_path}"

        debug_api(
            m=self.m,
            method='POST',
            url=f'{self.s.base_url}{call_url}',
            data=data,
            headers=headers,
        )

        try:
            response = check_response(
                m=self.m,
                cnf=cnf,
                response=self.s.post(
                    url=call_url, json=data, headers=headers, timeout=timeout,
                )
            )

        except HTTPX_EXCEPTIONS as error:
            api_pretty_exception(
                m=self.m, method='POST', error=error,
                url=f'{self.s.base_url}{call_url}',
            )
            raise

        return response

    def close(self) -> None:
        self.s.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
