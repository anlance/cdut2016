from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)

login = LoginManager(app=app)
login.login_view = 'login'

mail = Mail(app=app)

bootstrap = Bootstrap(app)

from app import routes, models, errors, mylog, mymail
