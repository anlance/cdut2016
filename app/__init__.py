import logging
from logging.handlers import SMTPHandler

from flask import Flask
from flask_apscheduler import APScheduler
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, lazy_gettext as _l

from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
scheduler = APScheduler()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- 初始化插件
    db.init_app(app)
    # migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    scheduler.init_app(app)

    # --- 注册蓝图
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.personal import bp as personal_bp
    app.register_blueprint(personal_bp, url_prefix='/personal')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.news_cdut import bp as news_cdut_bp
    app.register_blueprint(news_cdut_bp)

    from app.manage import bp as manage_bp
    app.register_blueprint(manage_bp, url_prefix='/manage')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Anlance Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    return app

