class ClientFailure(Exception):
    pass


class ModuleFailure(ClientFailure):
    pass


class ModuleSuccess(Exception):
    def __init__(self, result: dict):
        self.result = result
        super().__init__()


class ModuleHelp(Exception):
    def __init__(self, specs: dict):
        self.specs = specs
        super().__init__()
