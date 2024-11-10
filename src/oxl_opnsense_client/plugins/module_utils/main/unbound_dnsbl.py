from ..base.cls import GeneralModule


# Supported as of OPNsense 23.7
class DnsBL(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'unbound.dnsbl'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigureGeneral'
    FIELDS_CHANGE = [
        'enabled', 'safesearch', 'type', 'lists', 'whitelists', 'blocklists', 'wildcards', 'address', 'nxdomain'
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {
        'bool': ['enabled', 'safesearch', 'nxdomain'],
        'list': ['type', 'lists', 'whitelists', 'blocklists', 'wildcards'],
    }

    def __init__(self, m, result: dict):
        GeneralModule.__init__(self=self, m=m, r=result)

    def check(self) -> None:
        # pylint: disable=W0201
        self.settings = self._search_call()

        self._build_diff()
