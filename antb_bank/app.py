import json
import falcon

class HelloWorld(object):

    def on_get(self, req, resp):
        msg = {
            'content' : 'Hello World'
        }

        resp.body = json.dumps(msg, ensure_ascii=False)
        resp.status = falcon.HTTP_200



def register_app(api):
    hello_world = HelloWorld()
    api.add_route('/bank/accounts', hello_world)