import falcon
import json

api = app = falcon.API()

import antb_bank.app

antb_bank.app.register_app(api)