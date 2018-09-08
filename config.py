import os


class Config(object):
    SECRET_KEY ='you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:GSSG255211@localhost:3306/cdut2016?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True