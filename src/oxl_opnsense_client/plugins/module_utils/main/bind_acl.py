from ..helper.main import validate_str_fields, is_ip_or_network, is_unset
from ..base.cls import BaseModule


class Acl(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addAcl',
        'del': 'delAcl',
        'set': 'setAcl',
        'search': 'get',
        'toggle': 'toggleAcl',
    }
    API_KEY_PATH = 'acl.acls.acl'
    API_MOD = 'bind'
    API_CONT = 'acl'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['networks']
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['networks'],
    }
    STR_VALIDATIONS = {
        'name': r'^(?!any$|localhost$|localnets$|none$)[0-9a-zA-Z_\-]{1,32}$'
    }
    EXIST_ATTR = 'acl'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.acl = {}

    def check(self) -> None:
        validate_str_fields(
            m=self.m, data=self.p,
            field_regex=self.STR_VALIDATIONS,
        )

        if self.p['state'] == 'present':
            if is_unset(self.p['networks']):
                self.m.fail('You need to provide at networks to create an ACL!')

            for net in self.p['networks']:
                if not is_ip_or_network(net):
                    self.m.fail(
                        f"It seems you provided an invalid network: '{net}'"
                    )

        self._base_check()
