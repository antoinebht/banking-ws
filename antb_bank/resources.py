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


class Account(object):

    def __init__(self):
        self.db = storage.AccountsStorage()

    def on_get(self, req, resp, id):
        if not id.isdigit() :
            resp.body = ""
            resp.status = falcon.HTTP_BAD_REQUEST
            return 

        account = self.db.getAccount(int(id))
        if account == {} :
            resp.body = ""
            resp.status = falcon.HTTP_NOT_FOUND
        else :
            msg = account
            resp.body = json.dumps(msg, ensure_ascii=False)
            resp.status = falcon.HTTP_OK

