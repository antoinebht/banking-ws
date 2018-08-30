import falcon
from falcon import testing
import json
import pytest

from ws_root.app import api

@pytest.fixture
def client():
    return testing.TestClient(api)


def test_bank_accounts(client):
    msg = {
        'content': "Hello World"
    }

    response = client.simulate_get('/bank/accounts')
    res = json.loads(response.content)

    assert res == msg
    assert response.status == falcon.HTTP_OK

