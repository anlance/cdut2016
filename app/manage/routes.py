from datetime import datetime

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import null

from app import db
from app.manage import bp
from app.manage.form import ToWriteForm, TableForm
from app.models import User, admin_required, super_required, Announce, AnnounceModel


# 填写公告的name和info
@bp.route('/manage', methods=['GET', 'POST'])
@login_required
@admin_required
def manage():
    form = ToWriteForm()
    if form.validate_on_submit():
        name = form.name.data
        info = form.info.data
        item_num = form.item_num.data
        announce_modell = AnnounceModel(manage_id=current_user.id, name=name, info=info, item_num=item_num, up_time=datetime.now())
        db.session.add(announce_modell)
        db.session.commit()
        if announce_modell.item_num == 0:
            return render_template('manage/success.html', title='发布成功')
        cur_announce_model = AnnounceModel.query.filter(AnnounceModel.manage_id == current_user.id).order_by(AnnounceModel.up_time.desc()).first()
        return redirect(url_for('manage.add_announce', id=cur_announce_model.id))
    elif request.method == 'GET':
        announce_modell = AnnounceModel.query.filter(AnnounceModel.manage_id == current_user.id).order_by(AnnounceModel.up_time.desc()).first()
        print(announce_modell)
        if announce_modell is not None:
            form.name.data = announce_modell.name
            form.info.data = announce_modell.info
            form.item_num.data = announce_modell.item_num
        return render_template('manage/announce.html', title='管理中心', form=form)


# 填写公告的具体excel表格信息
@bp.route('/add_announce/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_announce(id):
    cur_announce_model = AnnounceModel.query.filter(AnnounceModel.id == id).first()
    form = TableForm()
    if form.is_submitted():
        i = 0
        while i < cur_announce_model.get_item_num():
            cur_announce_model[i] = form.items[i].itname.data, form.items[i].placeholder.data
            i += 1
        db.session.commit()
        return render_template('manage/success.html', title='发布成功', announce_model=cur_announce_model)
    else:
        for item in range(cur_announce_model.item_num):
            form.items.append_entry(item)
        return render_template('manage/add_announce.html', title='管理中心', form=form)


# 查询所有的用户
@bp.route('/allUser')
@login_required
@super_required
def allUser():
    user = User.query.filter(User.id > 1).all()
    return render_template('manage/allUser.html', user=user)


# 给与用户管理员权限
@bp.route('/be_manage/<id>')
@login_required
@super_required
def be_manage(id):
    user = User.query.filter(User.id > 1).all()
    be_user = User.query.filter_by(id=id).first_or_404()
    be_user.set_role(1)
    db.session.commit()
    flash(be_user.username+'已经成为管理员', 'success')
    return render_template('manage/allUser.html', user=user)


# 删除用户管理员权限
@bp.route('/del_manage/<id>')
@login_required
@super_required
def del_manage(id):
    user = User.query.filter(User.id > 1).all()
    del_manage = User.query.filter_by(id=id).first_or_404()
    del_manage.set_role(0)
    db.session.commit()
    flash(del_manage.username+'已经不是管理员', 'success')
    return render_template('manage/allUser.html', user=user)