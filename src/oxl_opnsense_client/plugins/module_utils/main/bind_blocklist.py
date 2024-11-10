from ..base.cls import GeneralModule


class Blocklist(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'dnsbl'
    API_MOD = 'bind'
    API_CONT = 'dnsbl'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'safe_google', 'safe_duckduckgo', 'safe_youtube', 'safe_bing',
        'exclude', 'block', 'enabled',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'block': 'type',
        'exclude': 'whitelists',
        'safe_google': 'forcesafegoogle',
        'safe_duckduckgo': 'forcesafeduckduckgo',
        'safe_youtube': 'forcesafeyoutube',
        'safe_bing': 'forcestrictbing',
    }
    FIELDS_BOOL_INVERT = ['ipv6', 'prefetch']
    FIELDS_TYPING = {
        'bool': [
            'safe_google', 'safe_duckduckgo', 'safe_youtube', 'safe_bing', 'enabled',
        ],
        'list': ['exclude', 'block'],
    }

    def __init__(self, m, result: dict):
        GeneralModule.__init__(self=self, m=m, r=result)
