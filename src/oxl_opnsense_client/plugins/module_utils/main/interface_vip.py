from ..helper.main import validate_int_fields
from ..base.cls import BaseModule


class Vip(BaseModule):
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY_PATH = 'vip.vip'
    API_MOD = 'interfaces'
    API_CONT = 'vip_settings'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'address', 'mode', 'expand', 'bind', 'gateway', 'password', 'vhid',
        'advertising_base', 'advertising_skew', 'description', 'interface',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'address': 'network',
        'expand': 'noexpand',
        'bind': 'nobind',
        'advertising_base': 'advbase',
        'advertising_skew': 'advskew',
        'description': 'descr',
    }
    FIELDS_DIFF_NO_LOG = ['password']
    FIELDS_BOOL_INVERT = ['expand', 'bind']
    FIELDS_TYPING = {
        'bool': ['expand', 'bind'],
        'select': ['mode', 'interface', 'vhid', 'advertising_base', 'advertising_skew'],
        'int': ['vhid', 'advertising_base', 'advertising_skew'],
    }
    INT_VALIDATIONS = {
        'vhid': {'min': 1, 'max': 255},
        'advertising_base': {'min': 1, 'max': 254},
        'advertising_skew': {'min': 0, 'max': 254},
    }
    EXIST_ATTR = 'vip'

    def __init__(self, m, result: dict):
        BaseModule.__init__(self=self, m=m, r=result)
        self.vip = {}

    def check(self) -> None:
        if self.p['address'].find('/') == -1:
            self.m.fail('The address needs to include a subnet CIDR!')

        if self.p['state'] == 'present':
            validate_int_fields(m=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        # pylint: disable=W0201
        self.existing_entries = self.get_existing()
        self._base_check()

    def update(self) -> None:
        self.b.update(enable_switch=False)

    # NOTE: workaround for OPNSense handling 'get' differently than 'add' and 'set'
    #   https://github.com/opnsense/core/issues/7041
    def get_existing(self) -> list:
        existing = []

        for entry in self.b.get_existing():
            entry['address'] = f"{entry['subnet']}/{entry['subnet_bits']}"
            entry.pop('subnet')
            entry.pop('subnet_bits')
            existing.append(entry)
            for field in self.FIELDS_BOOL_INVERT:
                entry[field] = not entry[field]

        return existing
