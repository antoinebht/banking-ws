import json
import falcon

from . import resources

def register_app(api):
    api.add_route('/bank/accounts', resources.Accounts())
    api.add_route('/bank/accounts/{id}', resources.Account())