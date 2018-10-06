import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import current_app

if not current_app.debug:
    if current_app.config['MAIL_SERVER']:
        auth = None
        if current_app.config['MAIL_USERNAME'] or current_app.config['MAIL_PASSWORD']:
            auth = (current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        secure = None
        if current_app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']),
            fromaddr='no-reply@' + current_app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        current_app.logger.addHandler(mail_handler)
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/anlance.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        current_app.logger.addHandler(file_handler)

        current_app.logger.setLevel(logging.INFO)
        current_app.logger.info('anlance startup')