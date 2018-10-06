from _md5 import md5
from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login, db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(160))
    email = db.Column(db.String(120), unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
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

    # def set_identity(self, identity):
    #     self.identity = identity
    #
    # def get_identity(self):
    #     return self.identity
    #
    # def set_deadtime_info(self, deadtime_info):
    #     self.deadtime_info = deadtime_info
    #
    # def get_deadtime_info(self):
    #     return self.deadtime_info
    #
    # def set_deadtime_day(self, deadtime_day):
    #     self.deadtime_day = deadtime_day
    #
    # def get_deadtime_day(self):
    #     return self.deadtime_day


class NewsConfig(db.Model):
    __tablename__ = 'newsconfig'
    id = db.Column(db.Integer, primary_key=True)
    cdut_total = db.Column(db.Integer)
    cdut_page_n = db.Column(db.Integer)

    def __init__(self, id, cdut_total, cdut_page_n):
        self.id = id
        self.cdut_total = cdut_total
        self.cdut_page_n = cdut_page_n

    # def set_cdut_total(self, cdut_total):
    #     self.cdut_total = cdut_total
    #
    # def get_cdut_total(self):
    #     return self.cdut_total


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
