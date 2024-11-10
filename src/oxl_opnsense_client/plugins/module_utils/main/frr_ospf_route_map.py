from ..helper.main import validate_int_fields, is_unset
from ..base.cls import BaseModule


class RouteMap(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addRoutemap',
        'del': 'delRoutemap',
        'set': 'setRoutemap',
        'search': 'get',
        'toggle': 'toggleRoutemap',
    }
    API_KEY_PATH = 'ospf.routemaps.routemap'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['action', 'id', 'prefix_list', 'set']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'prefix_list': 'match2',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['prefix_list'],
        'select': ['action'],
        'int': ['id'],
    }
    INT_VALIDATIONS = {
        'id': {'min': 10, 'max': 99},
    }
    EXIST_ATTR = 'route_map'
    SEARCH_ADDITIONAL = {
        'existing_prefixes': 'ospf.prefixlists.prefixlist',
    }

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.route_map = {}
        self.existing_prefixes = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['id']) or is_unset(self.p['action']):
                self.m.fail_json(
                    'To create a OSPF route-map you need to provide an ID and action!'
                )

            validate_int_fields(m=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()

        if self.p['state'] == 'present':
            self.b.find_multiple_links(
                field='prefix_list',
                existing=self.existing_prefixes,
            )

    def get_existing(self) -> list:
        existing = []

        for entry in self.b.get_existing():
            if len(entry['prefix_list']) > 0:
                _list = []
                for pre in entry['prefix_list']:
                    if pre in self.existing_prefixes:
                        _list.append(
                            self.existing_prefixes[pre]['name']
                        )

                entry['prefix_list'] = _list

            existing.append(entry)

        return existing
