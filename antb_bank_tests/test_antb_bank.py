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
        'accounts': [
            {'id': 1, 'name': "CCHQ1"},
            {'id': 2, 'name': "CCHQ2"}
        ]
    }

    response = client.simulate_get('/bank/accounts')
    res = json.loads(response.content)

    assert res == msg
    assert response.status == falcon.HTTP_OK


def test_bank_account_get(client):
    msg = {
        'id': 1, 
        'name': "CCHQ1",
        'periods' : [
            {
                'id': 1,
                'name': "period1",
                'operations' : [
                    { 'id': 1, 'date': "2018-06-26", 'amount': -123.26, 'tags' : ["INITIAL_VALUE"], 'checked': True}, 
                    { 'id': 2, 'date': "2018-06-27", 'amount':   26.08, 'tags' : ["REFUND", "HEALTH"], 'checked': False}, 
                    { 'id': 3, 'date': "2018-06-27", 'amount': 1149.42, 'tags' : ["SALARY"], 'checked': True}, 
                    { 'id': 4, 'date': "2018-06-28", 'amount':  -85.82, 'tags' : ["HOBBIES", "WITHDRAW"], 'checked': True}, 
                    { 'id': 5, 'date': "2018-06-29", 'amount':   -0.99, 'tags' : ["FREE"], 'checked': False}, 
                    { 'id': 6, 'date': "2018-06-30", 'amount':  -50.00, 'tags' : ["SAVING", "PEL"], 'checked': False}, 
                ]
            },
            {
                'id': 2,
                'name': "period2",
                'operations' : [
                    { 'id':  7, 'date': "2018-06-31", 'amount':  -540, 'tags' : ["RENT"], 'checked': True}, 
                    { 'id':  8, 'date': "2018-07-01", 'amount': 84.85, 'tags' : ["HELP", "PRIME_EMPLOI"], 'checked': False}, 
                    { 'id':  9, 'date': "2018-07-01", 'amount':  -7.6, 'tags' : ["HOBBIES", "CINEMA"], 'checked': True}, 
                    { 'id': 10, 'date': "2018-07-02", 'amount':  -5.6, 'tags' : ["FOOD", "SANDWICH"], 'checked': True}, 
                    { 'id': 11, 'date': "2018-07-08", 'amount':  -250, 'tags' : ["SAVING", "LIVA"], 'checked': False}, 
                    { 'id': 12, 'date': "2018-07-08", 'amount':  -50.00, 'tags' : ["SAVING", "PEL"], 'checked': False}, 
                ]
            }
        ]
    }

    response = client.simulate_get('/bank/accounts/10')
    assert response.status == falcon.HTTP_NOT_FOUND

    response = client.simulate_get('/bank/accounts/1S')
    assert response.status == falcon.HTTP_BAD_REQUEST 

    response = client.simulate_get('/bank/accounts/1')
    res = json.loads(response.content)
    assert res == msg
    assert response.status == falcon.HTTP_OK


def test_bank_account_post(client):
    name = 'CCHQ2'
    response = client.simulate_post(
        '/bank/accounts/'+name
    )
    res = json.loads(response.content)
    assert response.status == falcon.HTTP_CREATED
    assert not res == {}
    assert res['name'] == name

    response = client.simulate_get('/bank/accounts/'+str(res['id']))
    res2 = json.loads(response.content)
    assert response.status == falcon.HTTP_OK
    assert res == res2