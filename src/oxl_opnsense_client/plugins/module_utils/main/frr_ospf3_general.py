from ..base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'ospf6'
    API_MOD = 'quagga'
    API_CONT = 'ospf6settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'carp', 'id', 'enabled', 'redistribute',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'carp': 'carp_demote',
        'id': 'routerid',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'carp'],
        'list': ['redistribute'],
    }

    def __init__(self, m, result: dict):
        GeneralModule.__init__(self=self, m=m, r=result)
