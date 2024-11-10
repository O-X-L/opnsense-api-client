from ..helper.main import is_ip, valid_hostname, validate_port, is_true, is_unset
from ..helper.unbound import validate_domain
from ..base.cls import BaseModule


class DnsOverTls(BaseModule):
    CMDS = {
        'add': 'addDot',
        'del': 'delDot',
        'set': 'setDot',
        'search': 'get',
        'toggle': 'toggleDot',
    }
    API_KEY_PATH = 'unbound.dots.dot'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['domain', 'target', 'port', 'verify']
    FIELDS_ALL = ['type', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'target': 'server',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['port'],
    }
    EXIST_ATTR = 'dot'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.dot = {}

    def check(self) -> None:
        if not is_unset(self.p['domain']):
            validate_domain(m=self.m, domain=self.p['domain'])
        validate_port(m=self.m, port=self.p['port'])

        if not is_unset(self.p['verify']) and \
                not is_ip(self.p['verify']) and \
                not valid_hostname(self.p['verify']):
            self.m.fail(
                f"Verify-value '{self.p['verify']}' is neither a valid IP-Address "
                f"nor a valid hostname!"
            )

        if is_unset(self.p['domain']):
            self.b.find(match_fields=['target'])

        else:
            self.b.find(match_fields=['domain', 'target'])

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_call(self) -> list:
        dots = []
        raw = self.b.search()

        if len(raw) > 0:
            for uuid, dot in raw.items():
                if is_true(dot['type']['dot']['selected']):
                    dot.pop('type')
                    dot['uuid'] = uuid
                    dots.append(dot)

        return dots
