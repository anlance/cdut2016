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
    role = db.Column(db.Integer)
    username = db.Column(db.String(40))
    password = db.Column(db.String(160))
    email = db.Column(db.String(120), unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.now)
    identity = db.Column(db.String(100))
    school_number = db.Column(db.String(50))
    deadtime_info = db.Column(db.String(140))
    deadtime_day = db.Column(db.DateTime)
    score_num = db.Column(db.Integer)
    score = db.relationship("Score", backref="user")
    write = db.relationship("Announce", backref="user")

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


# 成绩
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


# 模板公告
class AnnounceModel(db.Model):
    __tablename__ = 'announceModel'
    id = db.Column(db.Integer, primary_key=True)
    manage_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    info = db.Column(db.String(500))
    item_num = db.Column(db.Integer)
    up_num = db.Column(db.Integer, default=0)
    up_time = db.Column(db.DateTime)
    item1 = db.Column(db.String(50))
    place1 = db.Column(db.String(50))
    item2 = db.Column(db.String(50))
    place2 = db.Column(db.String(50))
    item3 = db.Column(db.String(50))
    place3 = db.Column(db.String(50))
    item4 = db.Column(db.String(50))
    place4 = db.Column(db.String(50))
    item5 = db.Column(db.String(50))
    place5 = db.Column(db.String(50))
    item6 = db.Column(db.String(50))
    place6 = db.Column(db.String(50))
    item7 = db.Column(db.String(50))
    place7 = db.Column(db.String(50))
    item8 = db.Column(db.String(50))
    place8 = db.Column(db.String(50))
    item9 = db.Column(db.String(50))
    place9 = db.Column(db.String(50))
    item10 = db.Column(db.String(50))
    place10 = db.Column(db.String(50))
    item11 = db.Column(db.String(50))
    place11 = db.Column(db.String(50))
    item12 = db.Column(db.String(50))
    place12 = db.Column(db.String(50))
    item13 = db.Column(db.String(50))
    place13 = db.Column(db.String(50))
    item14 = db.Column(db.String(50))
    place14 = db.Column(db.String(50))
    item15 = db.Column(db.String(50))
    place15 = db.Column(db.String(50))
    item16 = db.Column(db.String(50))
    place16 = db.Column(db.String(50))
    item17 = db.Column(db.String(50))
    place17 = db.Column(db.String(50))
    item18 = db.Column(db.String(50))
    place18 = db.Column(db.String(50))
    item19 = db.Column(db.String(50))
    place19 = db.Column(db.String(50))
    item20 = db.Column(db.String(50))
    place20 = db.Column(db.String(50))

    def set_item_num(self, item_num):
        self.item_num = item_num

    def get_item_num(self):
        return self.item_num

    def __setitem__(self, key, value):
        if key == 0:
            self.item1 = value[0]
            self.place1 = value[1]
        elif key == 1:
            self.item2 = value[0]
            self.place2 = value[1]
        elif key == 2:
            self.item3 = value[0]
            self.place3 = value[1]
        elif key == 3:
            self.item4 = value[0]
            self.place4 = value[1]
        elif key == 4:
            self.item5 = value[0]
            self.place5 = value[1]
        elif key == 5:
            self.item6 = value[0]
            self.place6 = value[1]
        elif key == 6:
            self.item7 = value[0]
            self.place7 = value[1]
        elif key == 7:
            self.item8 = value[0]
            self.place8 = value[1]
        elif key == 8:
            self.item9 = value[0]
            self.place9 = value[1]
        elif key == 9:
            self.item10 = value[0]
            self.place10 = value[1]
        elif key == 10:
            self.item11 = value[0]
            self.place11 = value[1]
        elif key == 11:
            self.item12 = value[0]
            self.place12 = value[1]
        elif key == 12:
            self.item13 = value[0]
            self.place13 = value[1]
        elif key == 13:
            self.item14 = value[0]
            self.place14 = value[1]
        elif key == 14:
            self.item15 = value[0]
            self.place16 = value[1]
        elif key == 15:
            self.item16 = value[0]
            self.place16 = value[1]
        elif key == 16:
            self.item17 = value[0]
            self.place17 = value[1]
        elif key == 17:
            self.item18 = value[0]
            self.place18 = value[1]
        elif key == 18:
            self.item19 = value[0]
            self.place19 = value[1]
        elif key == 19:
            self.item20 = value[0]
            self.place20 = value[1]
        else:
            raise IndexError()

    def __getitem__(self, item):
        if item == 0:
            return [self.item1, self.place1]
        elif item == 1:
            return [self.item2, self.place2]
        elif item == 2:
            return [self.item3, self.place3]
        elif item == 3:
            return [self.item4, self.place4]
        elif item == 4:
            return [self.item5, self.place5]
        elif item == 5:
            return [self.item6, self.place6]
        elif item == 6:
            return [self.item7, self.place7]
        elif item == 7:
            return [self.item8, self.place8]
        elif item == 8:
            return [self.item9, self.place9]
        elif item == 9:
            return [self.item10, self.place10]
        elif item == 10:
            return [self.item11, self.place11]
        elif item == 11:
            return [self.item12, self.place12]
        elif item == 12:
            return [self.item13, self.place13]
        elif item == 13:
            return [self.item14, self.place14]
        elif item == 14:
            return [self.item15, self.place15]
        elif item == 15:
            return [self.item16, self.place16]
        elif item == 16:
            return [self.item17, self.place17]
        elif item == 17:
            return [self.item18, self.place18]
        elif item == 18:
            return [self.item19, self.place19]
        elif item == 19:
            return [self.item20, self.place20]
        else:
            raise IndexError()


# 用户填写的公告
class Announce(db.Model):
    __tablename__ = 'announce'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer)
    manage_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id = db.Column(db.Integer)
    item_num = db.Column(db.Integer)
    up_time = db.Column(db.DateTime)
    item1 = db.Column(db.String(140))
    item2 = db.Column(db.String(140))
    item3 = db.Column(db.String(140))
    item4 = db.Column(db.String(140))
    item5 = db.Column(db.String(140))
    item6 = db.Column(db.String(140))
    item7 = db.Column(db.String(140))
    item8 = db.Column(db.String(140))
    item9 = db.Column(db.String(140))
    item10 = db.Column(db.String(140))
    item11 = db.Column(db.String(140))
    item12 = db.Column(db.String(140))
    item13 = db.Column(db.String(140))
    item14 = db.Column(db.String(140))
    item15 = db.Column(db.String(140))
    item16 = db.Column(db.String(140))
    item17 = db.Column(db.String(140))
    item18 = db.Column(db.String(140))
    item19 = db.Column(db.String(140))
    item20 = db.Column(db.String(140))

    def __setitem__(self, key, value):
        if key == 0:
            self.item1 = value
        elif key == 1:
            self.item2 = value
        elif key == 2:
            self.item3 = value
        elif key == 3:
            self.item4 = value
        elif key == 4:
            self.item5 = value
        elif key == 5:
            self.item6 = value
        elif key == 6:
            self.item7 = value
        elif key == 7:
            self.item8 = value
        elif key == 8:
            self.item9 = value
        elif key == 9:
            self.item10 = value
        elif key == 10:
            self.item11 = value
        elif key == 11:
            self.item12 = value
        elif key == 12:
            self.item13 = value
        elif key == 13:
            self.item14 = value
        elif key == 14:
            self.item15= value
        elif key == 15:
            self.item16 = value
        elif key == 16:
            self.item17 = value
        elif key == 17:
            self.item18 = value
        elif key == 18:
            self.item19 = value
        elif key == 19:
            self.item20 = value
        else:
            raise IndexError()

    def __getitem__(self, item):
        if item == 0:
            return self.item1
        elif item == 1:
            return self.item2
        elif item == 2:
            return self.item3
        elif item == 3:
            return self.item4
        elif item == 4:
            return self.item5
        elif item == 5:
            return self.item6
        elif item == 6:
            return self.item7
        elif item == 7:
            return self.item8
        elif item == 8:
            return self.item9
        elif item == 9:
            return self.item10
        elif item == 10:
            return self.item11
        elif item == 11:
            return self.item12
        elif item == 12:
            return self.item13
        elif item == 13:
            return self.item14
        elif item == 14:
            return self.item15
        elif item == 15:
            return self.item16
        elif item == 16:
            return self.item17
        elif item == 17:
            return self.item18
        elif item == 18:
            return self.item19
        elif item == 19:
            return self.item20
        else:
            raise IndexError()


# 留言
class Discuss(db.Model):
    __tablename__ = 'discuss'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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
