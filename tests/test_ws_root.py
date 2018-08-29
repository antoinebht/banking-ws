import falcon
from falcon import testing
import json
import pytest

from ws_root.app import api

@pytest.fixture
def client():
    return testing.TestClient(api)


def test_hello_world(client):
    msg = {
        'content': "Hello World"
    }

    response = client.simulate_get('/hello_world')
    res = json.loads(response.content)

    assert res == msg
    assert response.status == falcon.HTTP_OK

