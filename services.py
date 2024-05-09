# services.py
from models import db, User


def create_user(name, username, password):
    new_user = User(name=name, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
