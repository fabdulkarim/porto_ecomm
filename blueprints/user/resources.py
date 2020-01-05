import hashlib

from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc

from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import admin_required, user_required

from datetime import datetime

from .model import Users
from blueprints import db, app

from . import *

bp_user = Blueprint('user', __name__)
api = Api(bp_user)


#CRUD untuk user, hanya bisa diakses admin
class UserEdit(Resource):
    
    @jwt_required
    @admin_required    
    def put(self, id):
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('alamat_kirim', location='json', required=True)
        parser.add_argument('status', location='json', required=True)

        args = parser.parse_args()

        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()

            qry.username = args['username']
            qry.email = args['email']
            qry.status = args['status'] #reaktivasi bisa lewat sini
            qry.alamat_kirim = args['alamat_kirim']
            qry.password = password_digest
            qry.updated_at = db.func.now()
            db.session.commit()

            return marshal(qry, Users.response_fields), 200
        return {'status': 'failed', 'result': str(validation)}, 400, {'Content-Type': 'application/json'}
        
    @jwt_required
    @admin_required
    def delete(self, id):

        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.status = False
        qry.updated_at = db.func.now()
        db.session.commit()

        return {'message': 'deleted'}, 200

    @jwt_required
    @admin_required
    def post(self):

        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        
        args = parser.parse_args()

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()
            
            user = Users(args['username'], args['email'], password_digest)

            try:
                db.session.add(user)
                db.session.commit()
            except:
                return {'status':'failed','message':'conflicting database'}, 409, {'Content-Type':'application/json'}
            app.logger.debug('DEBUG : %s', user)

            return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'failed', 'result': str(validation)}, 400, {'Content-Type': 'application/json'}
    
    @jwt_required
    @admin_required
    def get(self):
        qry = Users.query.all()

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        return marshal(qry, Users.response_fields), 200


#signup, terpisah
class UserSignUp(Resource):

    def post(self):

        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('alamat_kirim', location='json', required=True)
        
        args = parser.parse_args()

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()
            
            user = Users(args['username'], args['email'], password_digest, args['alamat_kirim'])

            try:
                db.session.add(user)
                db.session.commit()
            except:
                return {'status':'failed','message':'conflicting database'}, 409, {'Content-Type':'application/json'}
            app.logger.debug('DEBUG : %s', user)

            return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'failed', 'result': str(validation)}, 400, {'Content-Type': 'application/json'}

    #fitur perbarui data
    @jwt_required
    @user_required
    def put(self):
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('alamat_kirim', location='json', required=True)

        args = parser.parse_args()

        id = get_jwt_claims()['user_id']

        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()

            qry.username = args['username']
            qry.email = args['email']
            qry.alamat_kirim = args['alamat_kirim']
            qry.password = password_digest
            qry.updated_at = db.func.now()
            db.session.commit()

            return marshal(qry, Users.response_fields), 200
        return {'status': 'failed', 'result': str(validation)}, 400, {'Content-Type': 'application/json'}


api.add_resource(UserEdit, '/internal_user', '/internal_user/<int:id>')
api.add_resource(UserSignUp, '/daftar')