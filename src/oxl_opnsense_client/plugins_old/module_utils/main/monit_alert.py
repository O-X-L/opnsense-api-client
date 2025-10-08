from ..helper.main import validate_int_fields
from ..base.cls import BaseModule
from ..helper.validate import is_valid_email


class Alert(BaseModule):
    CMDS = {
        'add': 'addAlert',
        'del': 'delAlert',
        'set': 'setAlert',
        'search': 'get',
        'toggle': 'toggleAlert',
    }
    API_KEY_PATH = 'monit.alert'
    API_MOD = 'monit'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['recipient', 'not_on', 'events', 'format', 'reminder', 'description']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'not_on': 'noton',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'not_on'],
        'list': ['events'],
        'int': ['reminder'],
    }
    INT_VALIDATIONS = {
        'reminder': {'min': 0, 'max': 86400},
    }
    EXIST_ATTR = 'alert'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.alert = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(m=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

            if not is_valid_email(self.p['recipient']):
                self.m.fail(
                    f"The recipient value '{self.p['recipient']}' is not a "
                    f"valid email address!"
                )

        self._base_check()
