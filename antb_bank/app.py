import json
import falcon

from . import resources

def register_app(api):
    api.add_route('/bank/accounts', resources.Accounts())
    api.add_route('/bank/accounts/{account}', resources.Account())
    api.add_route('/bank/accounts/{account}/periods/{period_id}/operations', resources.Operations())
    api.add_route('/bank/accounts/{account}/periods/{period_id}/operations/{operation_id}', resources.Operation())