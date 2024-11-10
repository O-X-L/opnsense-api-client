from ..base.cls import BaseModule


class Loopback(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY_PATH = 'loopback.loopback'
    API_MOD = 'interfaces'
    API_CONT = 'loopback_settings'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = []
    FIELDS_ALL = [FIELD_ID]
    FIELDS_TYPING = {}
    EXIST_ATTR = 'interface'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.interface = {}

    def check(self) -> None:
        self._base_check()
