import ssl
from pathlib import Path
from json import JSONDecodeError
from json import dumps as json_dumps
from datetime import datetime


from ..defaults.main import DEBUG_CONFIG
from .main import ensure_list, is_ip
from .validate import is_valid_domain


def check_host(m) -> None:
    if not is_ip(m.params['firewall']):
        fw_dns = m.params['firewall']

        if fw_dns.find('.') == -1:
            # TLD-only will fail the domain validation
            fw_dns = f'dummy.{fw_dns}'

        if not is_valid_domain(fw_dns):
            m.fail(f"Host '{m.params['firewall']}' is neither a valid IP nor Domain-Name!")


def ssl_verification(m) -> (ssl.SSLContext, bool):
    context = ssl.create_default_context()

    if not m.params['ssl_verify']:
        context = False

    elif m.params['ssl_ca_file'] is not None:
        if Path(m.params['ssl_ca_file']).is_file():
            context.load_verify_locations(cafile=m.params['ssl_ca_file'])

        else:
            m.fail(f"Provided 'ssl_ca_file' at path '{m.params['ssl_ca_file']}' does not exist!")

    return context


def get_params_path(cnf: dict) -> str:
    params_path = ''

    if 'params' in cnf and cnf['params'] is not None:
        for param in ensure_list(cnf['params']):
            params_path += f"/{param}"

    return params_path


def _clean_response(response: dict) -> dict:
    response_data = response.copy()
    for field in [
        'headers', 'next_request', '_decoder', 'stream', 'extensions', 'history', 'is_closed',
        'is_stream_consumed', 'default_encoding',
    ]:
        if field in response_data:
            response_data.pop(field)

    return response_data


def debug_api(
        m, method: str = None, url: str = None,
        data: dict = None, headers: dict = None, response: dict = None,
) -> None:
    if 'debug' in m.params and m.params['debug']:
        if response is not None:
            msg = f"RESPONSE: '{_clean_response(response.__dict__)}'"

        else:
            msg = f'REQUEST: {method} | URL: {url}'

            if headers is not None:
                msg += f" | HEADERS: '{headers}'"

            if data is not None:
                msg += f" | DATA: '{json_dumps(data)}'"

            log_path = Path(DEBUG_CONFIG['path_log'])
            if not log_path.exists():
                log_path.mkdir()

            with open(
                    f"{log_path}/{DEBUG_CONFIG['log_api_calls']}",
                    'a+', encoding='utf-8'
            ) as log:
                log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')} | {msg}\n")

        m.info(msg)


def check_response(m, cnf: dict, response) -> dict:
    debug_api(m=m, response=response)

    if 'allowed_http_stati' not in cnf:
        cnf['allowed_http_stati'] = [200]

    try:
        json = response.json()

    except JSONDecodeError:
        json = {}

    if response.status_code not in cnf['allowed_http_stati'] or \
            ('result' in json and json['result'] == 'failed'):
        # sometimes an error 'hides' behind a 200-code
        if f"{response.__dict__}".find('Controller not found') != -1:
            m.fail(
                f"API call failed | Needed plugin not installed! | "
                f"Response: {response.__dict__}"
            )

        elif f"{response.__dict__}".find(' in use') != -1:
            json['in_use'] = True

        else:
            if 'validations' in json:
                m.fail(
                    f"API call failed | Error: {json['validations']} | "
                    f"Response: {response.__dict__}"
                )

            else:
                m.fail(f"API call failed | Response: {response.__dict__}")

    return json


def api_pretty_exception(m, method: str, url: str, error):
    call = f'{method} => {url}'
    msg = f"Unable to connect '{call}'"

    if str(error).find('timed out') != -1:
        msg = f"Got timeout calling '{call}'"

    if str(error).find('CERTIFICATE_VERIFY_FAILED') != -1 or str(error).find('certificate verify failed') != -1:
        msg = f"SSL verification failed '{url}'! Make sure to follow the the documentation: "\
              "https://opnsense.ansibleguy.net/en/latest/usage/2_basic.html#ssl-certificate"

    m.fail(f"{msg} ({error})")
