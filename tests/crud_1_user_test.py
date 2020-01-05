from flask import json, request

from . import app, call_client, create_token, client, reset_db, create_token_nonint

class TestUserCrud():

    reset_db() ### reset, and rebuild database, now empty

    def test_user_signup(self, client):
        data = {
            'username': 'mbaknya',
            'email': 'jhs@starlight.com',
            'password': 'secretjhs',
            'alamat_kirim': 'Jl. Simp. Taman Agung no.17, kamar Atas Tengah'
        }

        req = call_client(request)
        res = req.post('/daftar',
            json=data
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_user_signup_clone(self, client):
        data = {
            'username': 'mbaknya',
            'email': 'jhs@starlight.com',
            'password': 'secretjhs',
            'alamat_kirim': 'Jl. Simp. Taman Agung no.17, kamar Atas Tengah'
        }

        req = call_client(request)
        res = req.post('/daftar',
            json=data
        )

        res_json = json.loads(res.data)

        assert res.status_code == 409

    def test_user_signup_weakpass(self, client):
        data = {
            'username': 'mbaknya2',
            'email': 'jhs@starlight.com',
            'password': 'jhs',
            'alamat_kirim': 'Jl. Simp. Taman Agung no.17, kamar Atas Tengah'
        }

        req = call_client(request)
        res = req.post('/daftar',
            json=data
        )

        res_json = json.loads(res.data)

        assert res.status_code == 400

    def test_user_login(self, client):
        data = {
            'username': 'mbaknya',
            'password': 'secretjhs'
        }

        req = call_client(request)
        res = req.post('/login',
            json=data
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_user_update(self, client):
        token = create_token_nonint()

        data = {
            'username': 'mbaknya',
            'email': 'jhs@starlight.com',
            'password': 'secretjhs',
            'alamat_kirim': 'Jl. Simp. Taman Agung no.17, kamar Atas Tengah, bareng Fadhil'
        }

        req = call_client(request)
        res = req.put('/daftar',
            json=data,
            headers={'Authorization': 'Bearer ' + token}

        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_user_wrongaccount(self, client):
        token = create_token()

        data = {
            'username': 'mbaknya',
            'email': 'jhs@starlight.com',
            'password': 'secretjhs',
            'alamat_kirim': 'Jl. Simp. Taman Agung no.17, kamar Atas Tengah, bareng Fadhil'
        }

        req = call_client(request)
        res = req.put('/daftar',
            json=data,
            headers={'Authorization': 'Bearer ' + token}

        )

        res_json = json.loads(res.data)

        assert res.status_code == 403

    def test_useradmin_delete(self, client):
        token = create_token()

        req = call_client(request)
        res = req.delete('/internal_user/1',
            headers={'Authorization': 'Bearer ' + token}
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_useradmin_update(self,client):
        token = create_token()

        data = {
            'username': 'mbaknya',
            'email': 'jhs@starlight.com',
            'password': 'secretjhs',
            'alamat_kirim': 'Jl. Simp. Taman Agung no.17, kamar Atas Tengah',
            'status': 'True'
        }

        req = call_client(request)
        res = req.put('/internal_user/1',
            json = data,
            headers = {'Authorization': 'Bearer ' + token}

        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_useradmin_update_wrongid(self,client):
        token = create_token()

        data = {
            'username': 'mbaknya',
            'email': 'jhs@starlight.com',
            'password': 'secretjhs',
            'alamat_kirim': 'Jl. Simp. Taman Agung no.17, kamar Atas Tengah',
            'status': 'True'
        }

        req = call_client(request)
        res = req.put('/internal_user/2',
            json = data,
            headers = {'Authorization': 'Bearer ' + token}

        )

        res_json = json.loads(res.data)

        assert res.status_code == 404

    def test_useradmin_update_weakpass(self,client):
        token = create_token()

        data = {
            'username': 'mbaknya',
            'email': 'jhs@starlight.com',
            'password': 'jhs',
            'alamat_kirim': 'Jl. Simp. Taman Agung no.17, kamar Atas Tengah',
            'status': 'True'
        }

        req = call_client(request)
        res = req.put('/internal_user/1',
            json = data,
            headers = {'Authorization': 'Bearer ' + token}

        )

        res_json = json.loads(res.data)

        assert res.status_code == 400

    def test_useradmin_getall(self, client):
        token = create_token()

        req = call_client(request)
        res = req.get('/internal_user',

            headers = {'Authorization': 'Bearer ' + token}

        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_useradmin_wrongtoken(self, client):
        token = create_token_nonint()

        req = call_client(request)
        res = req.get('/internal_user',

            headers = {'Authorization': 'Bearer ' + token}

        )

        res_json = json.loads(res.data)

        assert res.status_code == 403

    def test_login_get(self, client):
        token = create_token()

        req = call_client(request)
        res = req.get('/login',
            headers = {'Authorization': 'Bearer ' + token}
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200
