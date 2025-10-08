from ..main.ipsec_auth import BaseAuth


class Auth(BaseAuth):
    CMDS = {
        'add': 'addLocal',
        'del': 'delLocal',
        'set': 'setLocal',
        'search': 'get',
        'toggle': 'toggleLocal',
    }
    API_KEY_PATH = 'swanctl.locals.local'

    def __init__(self, m, result: dict):
        BaseAuth.__init__(self=self, m=m, r=result)
        self.auth = {}
