from ..base.handler import ModuleSoftError
from ..helper.main import validate_int_fields
from ..helper.rule import validate_values
from ..base.cls import BaseModule


class Rule(BaseModule):
    CMDS = {
        'add': 'addRule',
        'del': 'delRule',
        'set': 'setRule',
        'search': 'get',
        'toggle': 'toggleRule',
    }
    API_KEY_PATH = 'filter.rules.rule'
    API_MOD = 'firewall'
    API_CONT = 'filter'
    FIELDS_CHANGE = [
        'sequence', 'action', 'quick', 'interface', 'direction',
        'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port',
        'destination_invert', 'destination_net', 'destination_port', 'log',
        'description', 'gateway',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'ip_protocol': 'ipprotocol',
        'source_invert': 'source_not',
        'destination_invert': 'destination_not',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'log', 'quick', 'source_invert', 'destination_invert'],
        'select': ['action', 'direction', 'ip_protocol', 'protocol', 'gateway'],
        'list': ['interface'],
    }
    EXIST_ATTR = 'rule'
    TIMEOUT = 60.0  # urltable etc reload
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 99999},
    }
    API_CMD_REL = 'apply'

    def __init__(
            self, m, result: dict, cnf: dict = None,
            fail_verify: bool = True, fail_proc: bool = True
    ):
        BaseModule.__init__(self=self, m=m, r=result)
        self.p = self.m.params if cnf is None else cnf  # to allow override by rule_multi
        self.fail_verify = fail_verify
        self.fail_proc = fail_proc
        self.rule = {}
        self.log_name = None

    def _build_log_name(self) -> str:
        if self.p['description'] not in [None, '']:
            log_name = self.p['description']

        else:
            log_name = f"{self.p['action'].upper()}: FROM "

            if self.p['source_invert']:
                log_name += 'NOT '

            log_name += f"{self.p['source_net']} <= PROTO {self.p['protocol']} => "

            if self.p['destination_invert']:
                log_name += 'NOT '

            log_name += f"{self.p['destination_net']}:{self.p['destination_port']}"

        return log_name

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(
                m=self.m,
                data=self.p,
                field_minmax=self.INT_VALIDATIONS,
                error_func=self._error
            )

        self._build_log_name()
        self.b.find(match_fields=self.p['match_fields'])

        if self.p['state'] == 'present':
            validate_values(
                error_func=self._error,
                m=self.m,
                cnf=self.p
            )
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _error(self, msg: str, verification: bool = True) -> None:
        if (verification and self.fail_verify) or (not verification and self.fail_proc):
            self.m.fail(msg)

        else:
            self.m.warn(msg)
            raise ModuleSoftError
