from ..helper.main import is_unset
from ..base.cls import BaseModule


class Pool(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'pool'
    API_MOD = 'ipsec'
    API_CONT = 'pools'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['network']
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {'network': 'addrs'}
    FIELDS_TYPING = {'bool': ['enabled']}
    EXIST_ATTR = 'pool'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.pool = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['network']):
                self.m.fail("You need to provide a 'network' to create an IPSec-Pool!")

        self._base_check()
