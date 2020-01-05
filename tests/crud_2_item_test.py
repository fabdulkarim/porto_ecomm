from flask import json, request

from . import app, call_client, create_token, client, reset_db

class TestItemCRUD():
    def test_item_create(self, client):
        token = create_token()

        data = {
            'name': 'Kyrie 5',
            'price': 1300000,
            'photo': 'https://photo.yupoo.com/huayi5198888/79769e71/22d35ca0.jpeg'
        }

        req = call_client(request)
        res = req.post('/item/internal',
            json=data,
            headers={'Authorization': 'Bearer ' + token}
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_item_delete(self, client):
        token = create_token()
        req = call_client(request)
        res = req.delete('/item/internal/1',
            headers={'Authorization': 'Bearer ' + token}
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_item_update(self, client):
        token = create_token()

        data = {
            'name': 'Kyrie 5',
            'price': 1300000,
            'photo': 'https://photo.yupoo.com/huayi5198888/79769e71/22d35ca0.jpeg',
            'status': True
        }

        req = call_client(request)
        res = req.put('/item/internal/1',
            json=data,
            headers={'Authorization': 'Bearer ' + token}
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_item_getall(self, client):
        token = create_token()

        req = call_client(request)
        res = req.get('/item/internal',
            headers={'Authorization': 'Bearer ' + token}
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200