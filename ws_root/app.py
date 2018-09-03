import falcon
import json
from falcon_cors import CORS

cors = CORS(allow_origins_list=['http://localhost:4200'],
            allow_all_headers=True,
            allow_all_methods=True)

api = app = falcon.API(middleware=[cors.middleware])


import antb_bank.app
antb_bank.app.register_app(api)