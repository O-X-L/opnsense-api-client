from ..helper.main import validate_int_fields, is_unset
from ..base.cls import BaseModule


class Community(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addCommunitylist',
        'del': 'delCommunitylist',
        'set': 'setCommunitylist',
        'search': 'get',
        'toggle': 'toggleCommunitylist',
    }
    API_KEY_PATH = 'bgp.communitylists.communitylist'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['number', 'seq', 'action', 'community']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'seq': 'seqnumber',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['action'],
    }
    INT_VALIDATIONS = {
        'number': {'min': 1, 'max': 500},
        'seq': {'min': 10, 'max': 99},
    }
    EXIST_ATTR = 'community_list'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.community_list = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['number']) or is_unset(self.p['seq']) or is_unset(self.p['action']):
                self.m.fail_json(
                    'To create a BGP community-list you need to provide a number, '
                    'sequence-number and action!'
                )

            validate_int_fields(m=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()
