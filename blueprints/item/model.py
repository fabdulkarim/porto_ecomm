from blueprints import db
from flask_restful import fields, inputs

class Items(db.Model):
    __tablename__ = "item"
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(255))
    purchased = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now())

    response_fields = {
        'item_id': fields.Integer,
        'name': fields.String,
        'price': fields.Integer,
        'purchased': fields.Integer,
        'photo':fields.String,
        'status': fields.Boolean,
        'created_at': fields.String,
        'updated_at': fields.String
    }

    def __init__(self, name, price, photo):
        self.name = name
        self.price = price
        self.status = True
        self.photo = photo
        self.purchased = 0

    def __repr__(self):
        return '<Item %r>' % self.name