import falcon
import json

class CorsMiddleware(object):
    def process_request(self, request, res):
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'DELETE,GET,HEAD,PATCH,POST,PUT')
        res.set_header('Access-Control-Expose-Headers', 'auth')
        res.set_header('Access-Control-Allow-Headers', 'auth')


api = app = falcon.API(middleware=[CorsMiddleware()])


import antb_bank.app
antb_bank.app.register_app(api)