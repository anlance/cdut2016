from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app import db
from app.manage.form import SubmitForm
from app.models import User, Score, AnnounceModel, Announce
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


# 编辑自己的信息
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


# 设置倒计时
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


# 成为超级管理员
@bp.route('/be_super/<id>',  methods=['GET', 'POST'])
@login_required
def be_super(id):
    user = User.query.filter_by(id=id).first_or_404()
    user.set_role(2)
    db.session.commit()
    flash("您已经是超级管理员了", "success")
    return render_template('personal/user.html', user=user)


# 查看自己的成绩单
@bp.route('/score', methods=['GET', 'POST'])
@login_required
def score():
    all_score = Score.query.filter_by(user_id=current_user.id).all()
    return render_template('personal/score.html', title='My Score', all_score=all_score)


# 可以不用登录就填写
# 填写表单
@bp.route('/submit/<announce_id>', methods=['GET', 'POST'])
def submit(announce_id):
    announce_model = AnnounceModel.query.filter(AnnounceModel.id == announce_id).first()
    form = SubmitForm()
    if form.is_submitted():
        i = 0
        manage_id = announce_model.manage_id
        item_num = announce_model.get_item_num()
        cur_announce = Announce(manage_id=manage_id, item_num=item_num, up_time=datetime.now())
        while i < announce_model.get_item_num():
            cur_announce[i] = form.items[i].item.data
            i += 1
        db.session.add(cur_announce)
        db.session.commit()
        return render_template('announces/success.html', title='提交成功', announce=cur_announce, announce_model=announce_model)
    else:
        for item in range(announce_model.item_num):
            form.items.append_entry(item)
        # 设置每个输入框的placeholder属性
        i = 0
        while i < announce_model.get_item_num():
            print(form.items[i].item)
            form.items[i].item.render_kw = {"placeholder": announce_model[i][1]}
            i += 1
        return render_template('announces/announce_base.html', title='管理中心', form=form, announce_model=announce_model)
