import falcon
import json

api = app = falcon.API()


class HelloWorld(object):

    def on_get(self, req, resp):
        msg = {
            'content' : 'Hello World'
        }

        resp.body = json.dumps(msg, ensure_ascii=False)
        resp.status = falcon.HTTP_200


hello_world = HelloWorld()
api.add_route('/hello_world', hello_world)