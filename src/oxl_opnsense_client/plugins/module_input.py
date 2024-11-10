from pathlib import Path
from .module_utils.base.handler import exit_cnf

TYPE_MAPPING = {
    'str': str,
    'bool': bool,
    'list': list,
    'int': int,
    'float': float,
    'dict': dict,
    'path': Path,
}

class ModuleInput:
    def __init__(self, client, params: dict, check_mode: bool = False):
        self.c = client
        self.user_params = params
        self.check_mode = check_mode

    @property
    def params(self):
        return {**self.c.params, **self.user_params}

    def info(self, msg: str):
        self.c.info(msg)

    def warn(self, msg: str):
        self.c.warn(msg)

    def fail(self, msg: str):
        self.c.fail(msg)

    def error(self, msg: str):
        self.c.error(msg)


# pylint: disable=R0915
def validate_input(i: ModuleInput, definition: dict):
    p = i.user_params
    if len(p) == 0:
        exit_cnf('No parameters/arguments provided')

    normalized_params = {}
    for k, d in definition.items():
        kn = k
        if k not in p and 'aliases' in d:
            for ka in d['aliases']:
                if ka in p:
                    kn = ka
                    break

        if kn not in p:
            if 'required' in d and d['required']:
                exit_cnf(f"The required parameter '{k}' was not provided!")

            if 'default' in d:
                normalized_params[k] = d['default']

            else:
                normalized_params[k] = ''

        else:
            normalized_params[k] = i.params[k]

        if 'type' in d:
            t = TYPE_MAPPING[d['type']]
            if not isinstance(normalized_params[k], t):
                try:
                    normalized_params[k] = t(normalized_params[k])

                except (TypeError, ValueError) as e:
                    exit_cnf(f"The parameter '{k}' has an invalid type - must be {d['type']} ({e})")

        if 'choices' in d:
            if isinstance(normalized_params[k], str) and normalized_params[k] not in d['choices']:
                exit_cnf(f"The parameter '{k}' has an invalid value - must be one of: {d['choices']}")

            elif isinstance(normalized_params[k], list):
                for e in normalized_params[k]:
                    if e not in d['choices']:
                        exit_cnf(
                            f"The parameter '{k}' has an invalid value - have to be one or multiple of: {d['choices']}"
                        )

    i.user_params = normalized_params


def empty_results() -> dict:
    return dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )


def valid_results(results: (dict, None)) -> dict:
    if not isinstance(results, dict):
        return empty_results()

    if 'changed' not in results or 'diff' not in results or \
            'before' not in results['diff'] or 'after' not in results['diff']:
        return empty_results()

    return results
