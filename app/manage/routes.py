from datetime import datetime
from io import BytesIO
from urllib.parse import quote

import xlsxwriter
from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user

from app import db
from app.manage import bp
from app.manage.form import ToWriteForm, TableForm
from app.models import User, admin_required, super_required, Announce, AnnounceModel


# 填写公告的name和info（新增加）
@bp.route('/manage', methods=['GET', 'POST'])
@login_required
@admin_required
def manage():
    form = ToWriteForm()
    if form.validate_on_submit():
        name = form.name.data
        info = form.info.data
        item_num = form.item_num.data
        announce_model = AnnounceModel(manage_id=current_user.id, name=name, info=info, item_num=item_num,
                                       up_time=datetime.now())
        db.session.add(announce_model)
        db.session.commit()
        flash("发布成功", "sucesss")
        if announce_model.item_num == 0:
            return render_template('manage/success.html', title='发布成功', announce_model=announce_model)
        cur_announce_model = AnnounceModel.query.filter(AnnounceModel.manage_id == current_user.id).order_by(
            AnnounceModel.up_time.desc()).first()
        return redirect(url_for('manage.add_announce', id=cur_announce_model.id))
    elif request.method == 'GET':
        announce_modell = AnnounceModel.query.filter(AnnounceModel.manage_id == current_user.id).order_by(
            AnnounceModel.up_time.desc()).first()
        if announce_modell is not None:
            form.name.data = announce_modell.name
            form.info.data = announce_modell.info
            form.item_num.data = announce_modell.item_num
    return render_template('manage/announce.html', title='管理中心', form=form)


# 查看填写的数据
@bp.route('/detail/<announce_model_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def detail(announce_model_id):
    announce_model = AnnounceModel.query.filter(AnnounceModel.id == announce_model_id).first()
    announces = Announce.query.filter(Announce.model_id == announce_model_id).all()
    return render_template('manage/detail.html', title='发布成功', announce_model=announce_model, announces=announces)


# 修改公告的name和info
@bp.route('/alter_model/<announceModel_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def alter_model(announceModel_id):
    form = ToWriteForm()
    announce_model = AnnounceModel.query.filter(
        AnnounceModel.id == announceModel_id and AnnounceModel.manage_id == current_user.id).order_by(
        AnnounceModel.up_time.desc()).first()
    if form.validate_on_submit():
        announce_model.name = form.name.data
        announce_model.info = form.info.data
        announce_model.item_num = form.item_num.data
        db.session.commit()
        flash("修改成功", "sucesss")
        if announce_model.item_num == 0:
            return render_template('manage/success.html', title='发布成功', announce_model=announce_model)
        cur_announce_model = AnnounceModel.query.filter(AnnounceModel.manage_id == current_user.id).order_by(
            AnnounceModel.up_time.desc()).first()
        return redirect(url_for('manage.add_announce', id=cur_announce_model.id))
    elif request.method == 'GET':
        if announce_model is not None:
            form.name.data = announce_model.name
            form.info.data = announce_model.info
            form.item_num.data = announce_model.item_num
        return render_template('manage/announce.html', title='修改告', form=form)


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
        flash("发布成功", "sucesss")
        return render_template('manage/success.html', title='发布成功', announce_model=cur_announce_model)
    else:
        for item in range(cur_announce_model.item_num):
            form.items.append_entry(item)
        i = 0
        while i < cur_announce_model.get_item_num():
            form.items[i].itname.data = cur_announce_model[i][0]
            form.items[i].placeholder.data = cur_announce_model[i][1]
            i += 1
        return render_template('manage/add_announce.html', title='管理中心', form=form, announce_model=cur_announce_model)


# 查询自己发布的公告
@bp.route('/look_announce/<manage_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def look_announce(manage_id):
    page = request.args.get('page', 1, type=int)
    announce_models = AnnounceModel.query.filter(AnnounceModel.manage_id == manage_id).order_by(
        AnnounceModel.up_time.desc()).paginate(page, 10, False)
    next_url = url_for('manage.look_announce', manage_id=current_user.id, page=announce_models.next_num) if announce_models.has_next else None
    prev_url = url_for('manage.look_announce', manage_id=current_user.id, page=announce_models.prev_num) if announce_models.has_prev else None
    return render_template('manage/look_announce.html', announce_models=announce_models.items, next_url=next_url,
                           prev_url=prev_url)


# 生成excel并且下载excel文件
@bp.route('/download/<announce_model_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def download(announce_model_id):
    announce_model = AnnounceModel.query.filter(AnnounceModel.id == announce_model_id).first()
    announces = Announce.query.filter(Announce.model_id == announce_model_id).all()
    out = BytesIO()
    workbook = xlsxwriter.Workbook(out)
    table = workbook.add_worksheet()
    for i in range(announce_model.up_num+1):
        for j in range(announce_model.item_num):
            if i == 0:
                table.write(i, j, announce_model[j][0])
            else:
                table.write(i, j, announces[i-1][j])
    workbook.close()
    out.seek(0)
    filename = quote(announce_model.name+".xlsx")
    rv = send_file(out, as_attachment=True, attachment_filename=filename)
    rv.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
    return rv
    # return send_file(out, as_attachment=True, attachment_filename="dream.xlsx")


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
    flash(be_user.username + '已经成为管理员', 'success')
    return render_template('manage/allUser.html', user=user)


# 删除用户管理员权限
@bp.route('/del_manage/<id>')
@login_required
@super_required
def del_manage(id):
    user = User.query.filter(User.id > 1).all()
    cur_manage = User.query.filter_by(id=id).first_or_404()
    cur_manage.set_role(0)
    db.session.commit()
    flash(cur_manage.username + '已经不是管理员', 'success')
    return render_template('manage/allUser.html', user=user)
