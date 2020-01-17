from blueprints import db
from flask_restful import fields, inputs

class Carts(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now())

    response_fields = {
        'id':fields.Integer,
        'user_id': fields.Integer,
        'item_id': fields.Integer,
        'status': fields.Boolean,
        'created_at': fields.String,
        'updated_at': fields.String
    }

    def __init__(self, user_id, item_id): 
        self.user_id = user_id
        self.item_id = item_id
        self.status = True

    def __repr__(self):
        return '<Cart %r>' % self.id

class Orders(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    transaksi = db.Column(db.String(30), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    alamatkirim = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now())

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'transaksi': fields.String,
        'total_price': fields.Integer,
        'alamatkirim': fields.String,
        'status': fields.Boolean,
        'created_at': fields.String,
        'updated_at': fields.String
    }

    def __init__(self, user_id, total_price, alamat_kirim): 
        self.user_id = user_id
        self.transaksi = "ORDER PLACED"
        self.total_price = total_price
        self.alamatkirim = alamat_kirim
        self.status = True

    def __repr__(self):
        return '<Order %r>' % self.id

class Details(db.Model):
    __tablename__ = "detail"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now())

    response_fields = {
        'id': fields.Integer,
        'order_id': fields.Integer,
        'item_id': fields.Integer,
        'quantity': fields.Integer,
        'status': fields.Boolean,
        'created_at': fields.String,
        'updated_at': fields.String
    }

    def __init__(self, order_id, item_id, quantity): 
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity
        self.status = True

    def __repr__(self):
        return '<Detail %r>' % self.id