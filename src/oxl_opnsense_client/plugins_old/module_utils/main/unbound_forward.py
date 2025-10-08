from ..helper.unbound import validate_domain
from ..helper.main import validate_port, is_true, is_unset
from ..base.cls import BaseModule


class Forward(BaseModule):
    CMDS = {
        'add': 'addForward',
        'del': 'delForward',
        'set': 'setForward',
        'search': 'get',
        'toggle': 'toggleForward',
    }
    API_KEY_PATH = 'unbound.dots.dot'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['domain', 'target', 'port']
    FIELDS_ALL = ['type', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'target': 'server',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['port'],
    }
    EXIST_ATTR = 'fwd'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.fwd = {}

    def check(self) -> None:
        if not is_unset(self.p['domain']):
            validate_domain(m=self.m, domain=self.p['domain'])

        validate_port(m=self.m, port=self.p['port'])

        self.b.find(match_fields=['domain', 'target'])

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_call(self) -> list:
        fwds = []
        raw = self.b.search()

        if len(raw) > 0:
            for uuid, dot in raw.items():
                if is_true(dot['type']['forward']['selected']):
                    dot.pop('type')
                    dot['uuid'] = uuid
                    fwds.append(dot)

        return fwds
