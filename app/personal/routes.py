from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app import db
from app.models import User
from app.personal import bp
from app.personal.form import EditProfileForm, DeadtimeForm


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'model': user.username, 'info': '1'},
        {'model': user.username, 'info': '2'}
    ]
    return render_template('personal/user.html', user=user, posts=posts)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.identity = form.identity.data
        current_user.school_number = form.school_number.data
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('personal.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.identity.data = current_user.identity
        form.school_number.data = current_user.school_number
    return render_template('personal/edit_profile.html', title='Edit Profile', form=form)


@bp.route('/set_deadtime', methods=['GET', 'POST'])
@login_required
def set_deadtime():
    form = DeadtimeForm(current_user.username)
    if form.validate_on_submit():
        current_user.deadtime_info = form.deadtime_info.data
        current_user.deadtime_day = form.deadtime_day.data
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('personal.user', username=current_user.username))
    elif request.method == 'GET':
        form.deadtime_info.data = current_user.deadtime_info
        form.deadtime_day.data = current_user.deadtime_day
    return render_template('personal/set_deadtime.html', title='Set Deadtime', form=form)


@bp.route('/be_super/<id>',  methods=['GET', 'POST'])
@login_required
def be_super(id):
    user = User.query.filter_by(id=id).first_or_404()
    user.set_role(2)
    db.session.commit()
    flash("您已经是超级管理员了", "success")
    return render_template('personal/user.html', user=user)