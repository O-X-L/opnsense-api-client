from .api import Session
from .base import Base
from ..helper.main import validate_int_fields, validate_str_fields


class SessionWrapper:
    def __init__(self, s: Session, timeout: float = None):
        self.s = s
        self.timeout = timeout

    def get(self, cnf: dict) -> dict:
        if self.timeout is not None:
            return self.s.get(cnf=cnf, timeout=self.timeout)

        return self.s.get(cnf=cnf)

    def post(self, cnf: dict, headers: dict = None) -> dict:
        if self.timeout is not None:
            return self.s.post(cnf=cnf, headers=headers, timeout=self.timeout)

        return self.s.post(cnf=cnf, headers=headers)

    def close(self):
        self.s.close()


class BaseModule:
    def __init__(self, m, r: dict):
        self.m = m
        self.s = SessionWrapper(
            s=self.m.c.session,
            timeout=self.TIMEOUT if hasattr(self, 'TIMEOUT') else None,
        )
        self.p = m.params
        self.r = r
        self.b = Base(instance=self)
        self.exists = False
        self.existing_entries = None
        self.call_cnf = {
            'module': self.b.i.API_MOD,
            'controller': self.b.i.API_CONT,
        }

    def _search_call(self) -> list:
        return self.b.search()

    def _base_check(self, match_fields: list = None):
        if match_fields is None:
            if 'match_fields' in self.p:
                match_fields = self.p['match_fields']

            elif hasattr(self, 'FIELD_ID'):
                match_fields = [self.FIELD_ID]

        if match_fields is not None:
            self.b.find(match_fields=match_fields)
            if self.exists:
                self.call_cnf['params'] = [getattr(self, self.EXIST_ATTR)[self.b.field_pk]]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def get_existing(self) -> list:
        return self.b.get_existing()

    def process(self) -> None:
        self.b.process()

    def create(self) -> None:
        self.b.create()

    def update(self) -> None:
        self.b.update()

    def delete(self) -> None:
        self.b.delete()

    def reload(self) -> None:
        self.b.reload()


class GeneralModule:
    # has only a single entry; cannot be deleted or created
    EXIST_ATTR = 'settings'

    def __init__(self, m, r: dict):
        self.m = m
        self.s = SessionWrapper(
            s=self.m.c.session,
            timeout=self.TIMEOUT if hasattr(self, 'TIMEOUT') else None,
        )
        self.p = m.params
        self.r = r
        self.b = Base(instance=self)
        self.exists = False
        self.existing_entries = None
        self.call_cnf = {
            'module': self.b.i.API_MOD,
            'controller': self.b.i.API_CONT,
        }
        self.settings = {}

    def check(self) -> None:
        if hasattr(self.b.i, 'STR_VALIDATIONS'):
            if hasattr(self.b.i, 'STR_LEN_VALIDATIONS'):
                validate_str_fields(
                    m=self.m,
                    data=self.p,
                    field_regex=self.b.i.STR_VALIDATIONS,
                    field_minmax_length=self.b.i.STR_LEN_VALIDATIONS
                )

            else:
                validate_str_fields(m=self.m, data=self.p, field_regex=self.b.i.STR_VALIDATIONS)

        elif hasattr(self.b.i, 'STR_LEN_VALIDATIONS'):
            validate_str_fields(m=self.m, data=self.p, field_minmax_length=self.b.i.STR_LEN_VALIDATIONS)

        if hasattr(self.b.i, 'INT_VALIDATIONS'):
            validate_int_fields(m=self.m, data=self.p, field_minmax=self.b.i.INT_VALIDATIONS)

        self.settings = self._search_call()
        self._build_diff()

    def _search_call(self) -> dict:
        return self.b.simplify_existing(self.b.search())

    def get_existing(self) -> dict:
        return self._search_call()

    def process(self) -> None:
        self.update()

    def update(self) -> None:
        self.b.update(enable_switch=False)

    def reload(self) -> None:
        self.b.reload()

    def _build_diff(self) -> None:
        self.r['diff']['before'] = self.b.build_diff(self.settings)
        self.r['diff']['after'] = self.b.build_diff({
            k: v for k, v in self.p.items() if k in self.settings
        })
