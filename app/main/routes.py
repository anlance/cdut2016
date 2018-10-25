from datetime import datetime

from flask import render_template, flash, redirect, request, url_for, jsonify, json
from flask_login import current_user, login_required

from app import db
from app.forms import DiscussForm
from app.main import bp
from app.main.forms import EditProfileForm, DeadtimeForm
from app.models import User, Discuss
from app.news_cdut.models import NewsCdut
from app.spider.today import get_today


@bp.before_request
@login_required
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@bp.route('/',  methods=['GET', 'POST'])
@bp.route('/index',  methods=['GET', 'POST'])
@login_required
def index():
    discuss_form = DiscussForm()
    news_cdut = NewsCdut.query.filter().order_by(NewsCdut.time.desc()).limit(5)
    user_said = Discuss.query.filter(Discuss.id > 1).all()
    today = get_today()
    return render_template('index.html', title='Home Page', news_cdut=news_cdut, today=today, user_said=user_said, discuss_form=discuss_form)


@bp.route('/be_super/<id>',  methods=['GET', 'POST'])
@login_required
def be_super(id):
    user = User.query.filter_by(id=id).first_or_404()
    user.set_role(2)
    db.session.commit()
    flash("您已经是超级管理员了", "success")
    return render_template('user.html', user=user)


@bp.route('/add_discuss',  methods=['POST'])
@login_required
def add_discuss():
    data = json.loads(request.form.get('data'))
    username = data['username']
    said = data['said']
    try:
        discuss = Discuss(username=username, said=said)
        db.session.add(discuss)
        db.session.commit()
    except Exception as err:
        flash(err+":发送失败", 'info')
    user_said = Discuss.query.filter(Discuss.id > 1).all()
    print(user_said)
    return jsonify({"success": 200, "user_said": [i.serialize() for i in user_said]})


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'model': user.username, 'info': '1'},
        {'model': user.username, 'info': '2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@bp.route('/set_deadtime', methods=['GET', 'POST'])
@login_required
def set_deadtime():
    form = DeadtimeForm(current_user.username)
    if form.validate_on_submit():
        current_user.deadtime_info = form.deadtime_info.data
        current_user.deadtime_day = form.deadtime_day.data
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.deadtime_info.data = current_user.deadtime_info
        form.deadtime_day.data = current_user.deadtime_day
    return render_template('set_deadtime.html', title='Set Deadtime', form=form)


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
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.identity.data = current_user.identity
        form.school_number.data = current_user.school_number
    return render_template('edit_profile.html', title='Edit Profile', form=form)


