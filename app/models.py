from _md5 import md5
from datetime import datetime
from functools import wraps
from time import time

import jwt
from flask import current_app, abort
from flask_login import UserMixin, current_user
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
    school_number = db.Column(db.String(50))
    deadtime_info = db.Column(db.String(140))
    deadtime_day = db.Column(db.DateTime)
    role = db.Column(db.Integer)
    score = db.relationship("Score", backref="user")

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

    def set_role(self, role):
        self.role = role

    def get_role(self):
        return self.role

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    term = db.Column(db.String(20))
    name = db.Column(db.String(100))
    teacher = db.Column(db.String(20))
    credit = db.Column(db.String(5))
    grade = db.Column(db.String(5))
    type = db.Column(db.String(20))
    gpa = db.Column(db.String(5))
    up_time = db.Column(db.DateTime)


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


# 管理员权限
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.get_role():
            abort(403)
        return func(*args, **kwargs)

    return decorated_function


# 超级管理员权限
def super_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if int(current_user.get_role()) < 2:
            abort(403)
        return func(*args, **kwargs)
    return decorated_function
