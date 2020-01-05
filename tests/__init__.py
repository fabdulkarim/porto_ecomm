import pytest
from app import app, cache
from flask import request, json
from blueprints import db

#### reset db func
def reset_db():
    db.drop_all()
    db.create_all()

## sebelum mulai, standar nulisnya gini, habis ini bisa dicoba ngecek coverage
#@pytest.fixture #sek sing iki masih ndak tahu flownya
def call_client(request):
    client = app.test_client()
    return client


@pytest.fixture  ### sing iki digenti karena fixture iki ra oleh dipanggil langsung
def client(request): ### sebagai fungsi sejajar
    return call_client(request)

#buat dulu fungsi yang bakal dipake terus, contoh, token
def create_token():
    token = cache.get('test-token')
    if token is None:
        #prepare data
        data = {
            "username": "admin",
            "password": "admin"
        }
        #do request
        req = call_client(request)
        res = req.post('/login',
            json=data,
            headers= {'Content-Type' : 'application/json'}
        )

        #untuk body pakai json dump, query langsung dict

        #store response
        res_json = json.loads(res.data)

        assert res.status_code == 200

        cache.set('test-token', res_json['token'], timeout=60)
        return res_json['token']
    else:
        return token

#non-internal client token
def create_token_nonint():
    token = cache.get('test-token-non-int')
    if token is None:
    #prepare data
        data = {
            'username': 'mbaknya',
            'password': 'secretjhs'
        }
        #do request
        req = call_client(request)
        res = req.post('/login',
            json=data
        )
        #store response
        res_json = json.loads(res.data)

        assert res.status_code == 200

        cache.set('test-token-nonint', res_json['token'], timeout=60)
        return res_json['token']
    else:
        return token

def test_get_token(self):
    token = create_token()

    req = call_client(request)
    res = req.get('/login',
        headers={'Authorization': 'Bearer ' + token}
    )

    assert res.status_code == 200