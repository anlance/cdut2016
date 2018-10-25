from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.manage import bp
from app.models import User, admin_required, super_required


@bp.route('/manage')
@login_required
@admin_required
def manage():
    return render_template('manage/announce.html')


@bp.route('/add_manage')
@login_required
@super_required
def add_manage():
    user = User.query.filter(User.id > 1).all()
    return render_template('manage/add_manage.html', user=user)


@bp.route('/be_manage/<id>')
@login_required
@super_required
def be_manage(id):
    user = User.query.filter(User.id > 1).all()
    be_user = User.query.filter_by(id=id).first_or_404()
    be_user.set_role(1)
    db.session.commit()
    flash(be_user.username+'已经成为管理员', 'success')
    return render_template('manage/add_manage.html', user=user)


@bp.route('/del_manage/<id>')
@login_required
@super_required
def del_manage(id):
    user = User.query.filter(User.id > 1).all()
    del_manage = User.query.filter_by(id=id).first_or_404()
    del_manage.set_role(0)
    db.session.commit()
    flash(del_manage.username+'已经不是管理员', 'success')
    return render_template('manage/add_manage.html', user=user)