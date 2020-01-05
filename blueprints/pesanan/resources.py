from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc

from flask_jwt_extended import jwt_required, get_jwt_claims #lupa
from blueprints import user_required

from datetime import datetime

from ..item.model import Items

from .model import Carts, Orders, Details
from blueprints import db, app

from . import *

bp_pesanan = Blueprint('pesanan', __name__)
api = Api(bp_pesanan)

#user CRUD/action for cart
class CartEdit(Resource):

    @jwt_required
    @user_required
    def get(self):

        qry = Carts.query

        #show only valid
        qry = qry.filter_by(status=True)

        #show only for current user
        id = get_jwt_claims()['user_id']
        qry = qry.filter_by(user_id=id)

        rows = []
        for row in qry:
            rows.append(marshal(row, Carts.response_fields))

        if len(rows) == 0:
            return {'message':'You have no Items in Cart'}, 200, {'Content-Type': 'application/json'}

        return rows, 200

    @jwt_required
    @user_required
    def post(self):
        user_id = get_jwt_claims()['user_id']

        parser = reqparse.RequestParser()
        parser.add_argument('item_id', location='json', required=True)
        args = parser.parse_args()
        cart = Carts(user_id,args['item_id'])

        db.session.add(cart)
        db.session.commit()

        return marshal(cart, Carts.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @user_required
    def delete(self, id):

        qry = Carts.query
        qry = qry.filter_by(id=id)

        us_id = get_jwt_claims()['user_id']
        qry = qry.filter_by(user_id=us_id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry = qry.first()
        qry.status = False
        qry.updated_at = db.func.now()
        db.session.commit()

        return {'message': 'deleted'}, 200

class DoTransaction(Resource):
    @jwt_required
    @user_required
    def post(self):
        #get user id from claims
        user_id = get_jwt_claims()['user_id']

        #get quantity from input json
        parser = reqparse.RequestParser()
        parser.add_argument('quantity', location='json', action='append', type=dict, required=True)
        parser.add_argument('alamat_kirim', location='json', required=True)

        args = parser.parse_args()
        
        list_masuk = list(args['quantity'])
        list_pair = []
        for item_quant in list_masuk:
            list_pair.append((int(item_quant['id']),int(item_quant['quant'])))
        dict_item_quant = dict(list_pair)

        qry = Carts.query.filter_by(status=True).filter_by(user_id=user_id)
        rows = []
        for que in qry:
            rows.append(marshal(que, Carts.response_fields))
        
        price_count = 0
        for marsh in rows:
            item_id = int(marsh['item_id'])
            qry2 = Items.query.get(item_id)
            item_marshal = marshal(qry2,Items.response_fields)
            price_count += item_marshal['price'] * dict_item_quant[item_id]
        order = Orders(user_id,price_count,args['alamat_kirim'])
        db.session.add(order)
        db.session.commit()

        order_marshal = marshal(order, Orders.response_fields)
        # done adding order
        # add details
        for marsh in rows:
            #add detail
            item_id = marsh['item_id']
            detail = Details(order_marshal['id'], item_id, dict_item_quant[item_id])
            db.session.add(detail)
            
            #delete cart item
            qry3 = Carts.query
            qry3 = qry3.filter_by(id=marsh['id'])

            qry3 = qry3.filter_by(user_id=user_id)

            if qry3 is None:
                return {'status': 'NOT_FOUND'}, 404

            qry3 = qry3.first()
            qry3.status = False
            qry3.updated_at = db.func.now()
            #commit for both details and cart delete
            db.session.commit()

        return order_marshal, 200

api.add_resource(CartEdit, '/cart', '/cart/<int:id>')
api.add_resource(DoTransaction, '/buynow')


    

