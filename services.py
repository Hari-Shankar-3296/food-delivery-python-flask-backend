# services.py
from models import db, User


def create_user(name, username, password, address, mobile):
    new_user = User(name=name, username=username, password=password, address=address, mobile=mobile)
    db.session.add(new_user)
    db.session.commit()
