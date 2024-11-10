from ..module_input import validate_input, ModuleInput, valid_results
from ..module_utils.helper.wrapper import module_wrapper
from ..module_utils.defaults.main import EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
from ..module_utils.main.bind_blocklist import Blocklist

BL_MAPPING = {
    'AdAway List': 'aa',
    'AdGuard List': 'ag',
    'Blocklist.site Ads': 'bla',
    'Blocklist.site Fraud': 'blf',
    'Blocklist.site Phishing': 'blp',
    'Cameleon List': 'ca',
    'Easy List': 'el',
    'EMD Malicious Domains List': 'emd',
    'Easyprivacy List': 'ep',
    'hpHosts Ads': 'hpa',
    'hpHosts FSA': 'hpf',
    'hpHosts PSH': 'hpp',
    'hpHosts PUP': 'hup',
    'Malwaredomain List': 'mw',
    'NoCoin List': 'nc',
    'PornTop1M List': 'pt',
    'Ransomware Tracker List': 'rw',
    'Simple Ad List': 'sa',
    'Simple Tracker List': 'st',
    'Steven Black List': 'sb',
    'WindowsSpyBlocker (spy)': 'ws',
    'WindowsSpyBlocker (update)': 'wsu',
    'WindowsSpyBlocker (extra)': 'wse',
    'YoYo List': 'yy',
}


def run_module(module_input: ModuleInput, result: dict = None) -> dict:
    result = valid_results(result)

    module_args = dict(
        block=dict(
            type='list', elements='str', required=False, choices=list(BL_MAPPING.keys()),
            aliases=['lists'], default=[],
            description="Blocklist's you want to enable"
        ),
        exclude=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['safe_list'],
            description='Domains to exclude from the filter'
        ),
        safe_google=dict(
            type='bool', required=False, default=False, aliases=['safe_search_google'],
        ),
        safe_duckduckgo=dict(
            type='bool', required=False, default=False, aliases=['safe_search_duckduckgo'],
        ),
        safe_youtube=dict(
            type='bool', required=False, default=False, aliases=['safe_search_youtube'],
        ),
        safe_bing=dict(
            type='bool', required=False, default=False, aliases=['safe_search_bing'],
        ),
        **EN_ONLY_MOD_ARG,
        **RELOAD_MOD_ARG,
    )

    validate_input(i=module_input, definition=module_args)
    module_wrapper(Blocklist(m=module_input, result=result))
    return result
