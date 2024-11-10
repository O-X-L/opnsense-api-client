from ..base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'bgp'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'as_number', 'id', 'graceful', 'enabled', 'networks',
        'redistribute',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'as_number': 'asnumber',
        'id': 'routerid',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'graceful'],
        'list': ['networks', 'redistribute'],
    }
    INT_VALIDATIONS = {
        'as_number': {'min': 1, 'max': 4294967295},
    }

    def __init__(self, m, result: dict):
        GeneralModule.__init__(self=self, m=m, r=result)
