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

    def on_get(self, req, resp, name):
        if not name.isdigit() :
            resp.body = ""
            resp.status = falcon.HTTP_BAD_REQUEST
            return 

        account = self.db.getAccount(int(name))
        if account == {} :
            resp.body = ""
            resp.status = falcon.HTTP_NOT_FOUND
        else :
            msg = account
            resp.body = json.dumps(msg, ensure_ascii=False)
            resp.status = falcon.HTTP_OK

    def on_post(self, req, resp, name) :
        account = self.db.addAccount(name)
        if account == {} :
            resp.body = ""
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
        else :
            msg = account
            resp.body = json.dumps(account, ensure_ascii=False)
            resp.status = falcon.HTTP_CREATED