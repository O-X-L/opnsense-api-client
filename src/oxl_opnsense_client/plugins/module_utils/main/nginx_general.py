from ..base.cls import GeneralModule


class General(GeneralModule):
    FIELD_ID = 'name'
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'nginx.general'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'nginx'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'enabled', 'ban_ttl',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    INT_VALIDATIONS = {
        'ban_ttl': {'min': 0},
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['ban_ttl'],
    }

    def __init__(self, m, result: dict):
        GeneralModule.__init__(self=self, m=m, r=result)
