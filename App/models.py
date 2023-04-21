from . import db
from flask_login import UserMixin
from datetime import datetime


class Trader(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    phone_number = db.Column(db.String(20))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    product = db.relationship("Product", backref="trader", passive_deletes=True)
    posts = db.relationship("Post", backref="trader", passive_deletes=True)

    def __init__(self, email, phone_number, username, password):
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.password = password


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20))
    description = db.Column(db.String(50))
    price = db.Column(db.String(10))
    filename = db.Column(db.Text, nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    product_owner = db.Column(db.Integer, db.ForeignKey("trader.id", ondelete="CASCADE"), nullable=False)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(30))
    phone_number = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    post_author = db.Column(db.Integer, db.ForeignKey("trader.id", ondelete="CASCADE"), nullable=False)

