from ..helper.main import validate_int_fields, is_ip_or_network, is_unset
from ..base.cls import BaseModule


class Network(BaseModule):
    CMDS = {
        'add': 'addNetwork',
        'del': 'delNetwork',
        'set': 'setNetwork',
        'search': 'get',
        'toggle': 'toggleNetwork',
    }
    API_KEY_PATH = 'ospf.networks.network'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['ip', 'mask', 'area', 'area_range', 'prefix_list_in', 'prefix_list_out']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'ip': 'ipaddr',
        'mask': 'netmask',
        'area_range': 'arearange',
        'prefix_list_in': 'linkedPrefixlistIn',
        'prefix_list_out': 'linkedPrefixlistOut',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['prefix_list_in', 'prefix_list_out'],
    }
    INT_VALIDATIONS = {
        'mask': {'min': 0, 'max': 32},
    }
    EXIST_ATTR = 'net'
    SEARCH_ADDITIONAL = {
        'existing_prefixes': 'ospf.prefixlists.prefixlist',
    }

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.net = {}
        self.existing_prefixes = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['area']):
                self.m.fail_json(
                    'To create a OSPF network you need to provide an area!'
                )

            if not is_ip_or_network(f"{self.p['ip']}/{self.p['mask']}", strict=True):
                self.m.fail_json(
                    'The combination of the provided ip and network mask is invalid: '
                    f"'{self.p['ip']}/{self.p['mask']}'!"
                )

            validate_int_fields(m=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()

        if self.p['state'] == 'present':
            self.b.find_single_link(
                field='prefix_list_in',
                existing=self.existing_prefixes,
            )
            self.b.find_single_link(
                field='prefix_list_out',
                existing=self.existing_prefixes,
            )

    def get_existing(self) -> list:
        existing = []

        for entry in self.b.get_existing():
            if entry['prefix_list_in'] not in [None, ''] and \
                    entry['prefix_list_in'] in self.existing_prefixes:
                entry['prefix_list_in'] = self.existing_prefixes[entry['prefix_list_in']]['name']

            if entry['prefix_list_out'] not in [None, ''] and \
                    entry['prefix_list_out'] in self.existing_prefixes:
                entry['prefix_list_out'] = self.existing_prefixes[entry['prefix_list_out']]['name']

            existing.append(entry)

        return existing
