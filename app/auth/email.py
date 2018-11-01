from flask import current_app, render_template

from app.mymail import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Anlance] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))


def send_score_update_email(user, score_list):
    send_email('[Anlance] 有新的成绩出来啦',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/new_score.txt', user=user, score_list=score_list),
               html_body=render_template('email/new_score.html', user=user, score_list=score_list))