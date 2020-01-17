from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc

from flask_jwt_extended import jwt_required #lupa
from blueprints import admin_required, user_required

from datetime import datetime

from .model import Items
from blueprints import db, app

from . import *

bp_item = Blueprint('item', __name__)
api = Api(bp_item)

#begin CRUD item

class ItemEditAdmin(Resource):
    
    @jwt_required
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('photo', location='json', required=True)
        
        args = parser.parse_args()

        item = Items(args['name'],args['price'],args['photo'])

        db.session.add(item)
        db.session.commit()
        return marshal(item, Items.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @admin_required
    def get(self):
        
        qry = Items.query.all()

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        return marshal(qry, Items.response_fields), 200

    @jwt_required
    @admin_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('photo', location='json', required=True)
        parser.add_argument('status', location='json', type=bool, required=True)


        args = parser.parse_args()

        qry = Items.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.name = args['name']
        qry.price = args['price']
        qry.photo = args['photo']
        qry.status = args['status']
        qry.updated_at = db.func.now()
        db.session.commit()

        return marshal(qry, Items.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @admin_required
    def delete(self, id):

        qry = Items.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.status = False
        qry.updated_at = db.func.now()
        db.session.commit()

        return {'message': 'deleted'}, 200

class PublicItem(Resource):
    def get(self):
        
        qry = Items.query.all()

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        return marshal(qry, Items.response_fields), 200

    def options(self):
        return {}, 200

class PublicGetSpecific(Resource):
    def get(self,id):
        
        qry = Items.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        return marshal(qry, Items.response_fields), 200

    def options(self):
        return {}, 200

api.add_resource(ItemEditAdmin, '/internal/<int:id>','/internal')
api.add_resource(PublicItem, '')
api.add_resource(PublicGetSpecific, '/<int:id>')
