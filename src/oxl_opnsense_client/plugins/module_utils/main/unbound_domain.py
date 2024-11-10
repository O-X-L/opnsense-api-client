from ..helper.main import validate_port, is_ip
from ..helper.unbound import validate_domain
from ..base.cls import BaseModule


class Domain(BaseModule):
    CMDS = {
        'add': 'addDomainOverride',
        'del': 'delDomainOverride',
        'set': 'setDomainOverride',
        'search': 'get',
        'toggle': 'toggleDomainOverride',
    }
    API_KEY_PATH = 'unbound.domains.domain'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['domain', 'server', 'description']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
    }
    EXIST_ATTR = 'domain'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.domain = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_domain(m=self.m, domain=self.p['domain'])
            self._validate_server()

        self._base_check()

    def _validate_server(self) -> None:
        server = self.p['server']

        if server.find('@') != -1:
            server, port = self.p['server'].split('@', 1)
            validate_port(m=self.m, port=port)

        if not is_ip(server):
            self.m.fail_json(f"Value '{server}' is not a valid IP-address!")
