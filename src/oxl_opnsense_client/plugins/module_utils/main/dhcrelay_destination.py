from ..helper.main import is_unset
from ..base.cls import BaseModule


class DhcRelayDestination(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addDest',
        'del': 'delDest',
        'set': 'setDest',
        'search': 'get',
    }
    API_KEY_PATH = 'dhcrelay.destinations'
    API_KEY_PATH_REQ = 'destination'
    API_MOD = 'dhcrelay'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['server']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'list': ['server'],
    }
    EXIST_ATTR = 'destination'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.destination = {}

    def check(self) -> None:

        if self.p['state'] == 'present':
            if is_unset(self.p['server']):
                self.m.fail_json("You need to provide list of 'server' to create a dhcrelay_destination!")

        self._base_check()
