# services.py
from models import db, User


def create_user(name, username, password, address, mobile, user_type):
    new_user = User(name=name, username=username, password=password, address=address, mobile=mobile, type=user_type)
    db.session.add(new_user)
    db.session.commit()
