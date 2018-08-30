import json
import falcon
from . import storage

class Accounts(object):

    def __init__(self):
        self.db = storage.AccountsStorage()

    def on_get(self, req, resp):
        msg = {
            'accounts' : self.db.getAccounts()
        }

        resp.body = json.dumps(msg, ensure_ascii=False)
        resp.status = falcon.HTTP_200

