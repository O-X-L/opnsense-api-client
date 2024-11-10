from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.unbound_dnsbl import DnsBL


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        safesearch=dict(
            type='bool', required=False, default=False,
            description='Force the usage of SafeSearch on Google, DuckDuckGo, Bing, Qwant, PixaBay and YouTube'
        ),
        type=dict(
            type='list', elements='str', required=False, default=[], aliases=['bl'],
            description='Select which kind of DNSBL you want to use'
        ),
        lists=dict(
            type='list', elements='str', required=False, default=[], aliases=['list'],
            description='List of urls from where blocklist will be downloaded'
        ),
        whitelists=dict(
            type='list', elements='str', required=False, default=[], aliases=['whitelist', 'allowlist', 'allowlists'],
            description='List of domains to whitelist. You can use regular expressions'
        ),
        blocklists=dict(
            type='list', elements='str', required=False, default=[], aliases=['blocklist'],
            description='List of domains to blocklist. Only exact matches are supported'
        ),
        wildcards=dict(
            type='list', elements='str', required=False, default=[], aliases=['wildcard'],
            description='List of wildcard domains to blocklist. All subdomains of the given domain will be blocked. '
                        'Blocking first-level domains is not supported'
        ),
        address=dict(
            type='str', required=False,
            description='Destination ip address for entries in the blocklist (leave empty to use default: 0.0.0.0). '
                        'Not used when "Return NXDOMAIN" is checked'
        ),
        nxdomain=dict(
            type='bool', required=False, default=False,
            description='Use the DNS response code NXDOMAIN instead of a destination address'
        ),
        **EN_ONLY_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(DnsBL(m=module_input, result=result))
    return result
