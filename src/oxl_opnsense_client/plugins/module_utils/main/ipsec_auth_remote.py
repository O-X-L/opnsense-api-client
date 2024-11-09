from ..base.api import     Session
from ..main.ipsec_auth import     BaseAuth


class Auth(BaseAuth):
    CMDS = {
        'add': 'addRemote',
        'del': 'delRemote',
        'set': 'setRemote',
        'search': 'get',
        'toggle': 'toggleRemote',
    }
    API_KEY_PATH = 'swanctl.remotes.remote'

    def __init__(self, m, result: dict, session: Session = None):
        BaseAuth.__init__(self=self, m=m, r=result, s=session)
        self.auth = {}
