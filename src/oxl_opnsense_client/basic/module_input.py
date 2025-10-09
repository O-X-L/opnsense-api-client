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


def empty_results() -> dict:
    return dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )


def valid_results(results: dict) -> dict:
    if not isinstance(results, dict):
        return empty_results()

    if 'changed' not in results or 'diff' not in results or \
            'before' not in results['diff'] or 'after' not in results['diff']:
        return empty_results()

    return results
