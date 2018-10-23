from _md5 import md5
from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login, db


# 用户
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(160))
    email = db.Column(db.String(120), unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.now)
    identity = db.Column(db.String(100))
    deadtime_info = db.Column(db.String(140))
    deadtime_day = db.Column(db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


# 留言
class Discuss(db.Model):
    __tablename__ = 'discuss'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    said = db.Column(db.String(140))
    saidtime = db.Column(db.DateTime, default=datetime.now())

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'said': self.said,
            'saidtime': self.saidtime,
        }


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
