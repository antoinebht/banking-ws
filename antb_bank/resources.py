import json
import re
import falcon
from . import storage

class Accounts(object):

    def __init__(self):
        self.db = storage.AccountsStorage()

    def on_get(self, req, resp):
        msg = self.db.getAccounts()
        resp.body = json.dumps(msg, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Account(object):

    def __init__(self):
        self.db = storage.AccountsStorage()

    def on_get(self, req, resp, account):
        if not account.isdigit() :
            resp.body = ""
            resp.status = falcon.HTTP_BAD_REQUEST
            return 

        acc = self.db.getAccount(int(account))
        if acc == {} :
            resp.body = ""
            resp.status = falcon.HTTP_NOT_FOUND
        else :
            msg = acc
            resp.body = json.dumps(msg, ensure_ascii=False)
            resp.status = falcon.HTTP_OK

    def on_post(self, req, resp, account) :
        acc = self.db.addAccount(account)
        if acc == {} :
            resp.body = ""
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
        else :
            resp.body = json.dumps(acc, ensure_ascii=False)
            resp.status = falcon.HTTP_CREATED

class Operations(object):
    def __init__(self):
            self.db = storage.AccountsStorage()

    def on_post(self, req, resp, account, period_id):
        if not account.isdigit() or not period_id.isdigit() :
            resp.body = ""
            resp.status = falcon.HTTP_BAD_REQUEST
            return 
        account = int(account)
        period_id = int(period_id)

        if req.content_length:
            op = json.load(req.stream)
        else :
            resp.body = ""
            resp.status = falcon.HTTP_BAD_REQUEST
            return 

        date_pattern = re.compile("^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$")
        if not date_pattern.match(op['date']):
            resp.body = ""
            resp.status = falcon.HTTP_BAD_REQUEST
            return 

        operation = self.db.addOperation(account, period_id, op['date'], op['amount'], op['tags'], op['checked'])
        if operation == {} :
            resp.body = ""
            resp.status = falcon.HTTP_NOT_FOUND
        else :
            msg = operation
            resp.body = json.dumps(operation, ensure_ascii=False)
            resp.status = falcon.HTTP_CREATED

class Operation(object):
    def __init__(self):
            self.db = storage.AccountsStorage()

    def on_put(self, req, resp, account, period_id, operation_id):
        if not account.isdigit() or not period_id.isdigit() or not operation_id.isdigit():
            resp.body = ""
            resp.status = falcon.HTTP_BAD_REQUEST
            return 
        account = int(account)
        period_id = int(period_id)
        operation_id = int(operation_id)

        if req.content_length:
            op = json.load(req.stream)
        else :
            resp.body = ""
            resp.status = falcon.HTTP_BAD_REQUEST
            return 

        date_pattern = re.compile("^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$")
        if not date_pattern.match(op['date']):
            resp.body = ""
            resp.status = falcon.HTTP_BAD_REQUEST
            return 

        operation = self.db.updateOperation(account, period_id, operation_id, op['date'], op['amount'], op['tags'], op['checked'])
        if operation == {} :
            resp.body = ""
            resp.status = falcon.HTTP_NOT_FOUND
        else :
            msg = operation
            resp.body = json.dumps(operation, ensure_ascii=False)
            resp.status = falcon.HTTP_OK

    def on_delete(self, req, resp, account, period_id, operation_id):
        pass