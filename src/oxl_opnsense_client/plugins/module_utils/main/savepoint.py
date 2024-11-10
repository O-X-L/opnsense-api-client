class SavePoint:
    def __init__(self, m, result: dict, controller: str = None):
        self.m = m
        self.r = result
        self.c = controller if controller is not None else self.m.params['controller']
        self.revision = self.m.params['revision']
        self.call_cnf = {
            'module': self.m.params['api_module'],
            'controller': self.c,
        }

    def create(self) -> str:
        if not self.m.check_mode:
            if self.revision is None:
                response = self.m.c.session.post(
                    cnf={
                        'command': 'savepoint',
                        **self.call_cnf,
                    }
                )

                if 'revision' not in response:
                    self.m.fail(msg='Failed to create savepoint!')

                return response['revision']

            self.m.fail(f"Unable to create savepoint - a revision ('{self.revision}') exists!")

    def _check_revision(self, action: str) -> None:
        if self.revision is None:
            self.m.fail(f"Unable to run action '{action}' - a target revision needs to be provided!")

    def apply(self) -> None:
        if not self.m.check_mode:
            self._check_revision(action='apply')
            self.m.c.session.post(
                cnf={
                    'command': 'apply',
                    'params': [self.revision],
                    **self.call_cnf,
                }
            )

    def cancel_rollback(self) -> None:
        if not self.m.check_mode:
            self._check_revision(action='cancel_rollback')
            self.m.c.session.post(
                cnf={
                    'command': 'cancelRollback',
                    'params': [self.revision],
                    **self.call_cnf,
                }
            )

    def revert(self) -> None:
        if not self.m.check_mode:
            self._check_revision(action='revert')
            self.m.c.session.post(
                cnf={
                    'command': 'revert',
                    'params': [self.revision],
                    **self.call_cnf,
                }
            )
