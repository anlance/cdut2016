import os


class Config(object):
    # FLASK_DEBUG = 0
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:GSSG255211@localhost:3306/cdut2016?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['cdut@anlan.club']
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'cdut@anlan.club'
    MAIL_PASSWORD = 'GSSG255211dud'
    #
    # LANGUAGES = ['en', 'zh-cn']POSTS_PER_PAGE = 3

    NEWS_PER_PAGE = 5

    SCHEDULER_API_ENABLED = True
    # JOBS = [
    #     {
    #         'id': 'job1',
    #         'func': 'app.task:save',
    #         'args': '',
    #         'trigger': {
    #             'type': 'cron',
    #             'second': '*/(60*60)'
    #         }
    #
    #     }
    # ]


