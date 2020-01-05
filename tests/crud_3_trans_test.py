from flask import json, request

from . import app, call_client, create_token, client, reset_db, create_token_nonint

class TestCartUser():

    def test_cart_getallempty(self, client):
        token = create_token_nonint()

        req = call_client(request)
        res = req.get('/cart',
            headers={'Authorization': 'Bearer ' + token}
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_cart_add(self,client):
        token = create_token_nonint()

        data = {
            'item_id':1
        }

        req = call_client(request)
        res = req.post('/cart',
            json=data,
            headers={'Authorization': 'Bearer ' + token}
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_cart_delete(self, client):
        token = create_token_nonint()

        req = call_client(request)
        res = req.delete('/cart/1',
            headers={'Authorization': 'Bearer ' + token}
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

class TestMainTrans():
    def test_do_trans(self, client):
        tokenadmin = create_token()
        tokenuser = create_token_nonint()

        data1 = {
            'name': 'Don 1',
            'price': 1000000,
            'photo': 'https://photo.yupoo.com/huayi5198888/1530576b/48848301.jpeg'
        }

        req = call_client(request)
        res = req.post('/item/internal',
            json=data1,
            headers={'Authorization': 'Bearer ' + tokenadmin}
        )

        data2 = {
            'item_id':1
        }

        req = call_client(request)
        res = req.post('/cart',
            json=data2,
            headers={'Authorization': 'Bearer ' + tokenuser}
        )

        data3 = {
            'item_id':2
        }

        req = call_client(request)
        res = req.post('/cart',
            json=data3,
            headers={'Authorization': 'Bearer ' + tokenuser}
        )

        data4 = {
	    "quantity":[
            {
                "id":1,
                "quant":1
            },
            {
                "id":2,
                "quant":2
            }
            ],
	    "alamat_kirim":"Jalan Tidar no.23"
        }

        req = call_client(request)
        res = req.post('/buynow',
            json=data4,
            headers={'Authorization': 'Bearer ' + tokenuser}
        )

        assert res.status_code == 200

class TestInfoOrder():
    def test_user_check(self, client):
        token = create_token_nonint()

        req = call_client(request)
        res = req.get('/buynow',
            headers={'Authorization': 'Bearer ' + token}
        )

        assert res.status_code == 200

    def test_admin_check(self, client):
        token = create_token()

        req = call_client(request)
        res = req.get('/internal_trans',
            headers={'Authorization': 'Bearer ' + token}
        )

        assert res.status_code == 200

    def test_admin_edit(self, client):
        token = create_token()

        data = {
            'transaksi':'DIBAYAR'
        }
        req = call_client(request)
        res = req.put('/internal_trans/1',
            json=data,
            headers={'Authorization': 'Bearer ' + token}
        )

        assert res.status_code == 200