from ..base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'general'
    API_MOD = 'quagga'
    API_CONT = 'general'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'enabled', 'profile', 'carp', 'log', 'snmp_agentx', 'log_level',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'carp': 'enablecarp',
        'log': 'enablesyslog',
        'snmp_agentx': 'enablesnmp',
        'log_level': 'sysloglevel',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'carp', 'log', 'snmp_agentx'],
        'select': ['log_level', 'profile'],
    }

    def __init__(self, m, result: dict):
        GeneralModule.__init__(self=self, m=m, r=result)
