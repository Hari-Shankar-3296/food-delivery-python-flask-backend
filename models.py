# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    address = db.Column(db.String)
    mobile = db.Column(db.String)
    type = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    address = db.Column(db.String)
    mobile = db.Column(db.String)
    image_url = db.Column(db.String, default="https://placehold.co/js/main.js?id=a724dadcca62e6c347623dd51681d1fb")
    reviews = db.Column(db.String, default="Delicious food with reasonable price")
    distance = db.Column(db.String, default="10 km")
    expected_delivery_time = db.Column(db.String, default="30 minutes")
    cuisine = db.Column(db.String)
    open_time = db.Column(db.String, default="9:00 AM")
    close_time = db.Column(db.String, default="9:00 PM")
    rating = db.Column(db.Double, default=4.0)
    offers = db.Column(db.String, default="Free food devilery")
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class DeliveryPartner(db.Model):
    __tablename__ = 'delivery_partners'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    mobile = db.Column(db.String)
    rating = db.Column(db.Float, default=4.0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    name = db.Column(db.String)
    description = db.Column(db.String)
    image_url = db.Column(db.String, default="https://placehold.co/js/main.js?id=a724dadcca62e6c347623dd51681d1fb")
    price = db.Column(db.Float)
    rating = db.Column(db.Float, default=4.0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)