from datetime import datetime

from flask import render_template, flash, redirect, request, url_for, jsonify, json
from flask_login import current_user, login_required

from app import db
from app.forms import DiscussForm
from app.main import bp
from app.main.forms import EditProfileForm
from app.models import User, Discuss
from app.news_cdut.models import NewsCdut
from app.spider.today import get_today


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@bp.route('/',  methods=['GET', 'POST'])
@bp.route('/index',  methods=['GET', 'POST'])
@login_required
def index():
    discuss_form = DiscussForm()
    # if discuss_form.validate_on_submit():
    #     username = discuss_form.username.data
    #     said = discuss_form.said.data
    #     discuss = Discuss(username=username, said=said)
    #     db.session.add(discuss)
    #     db.session.commit()
    news_cdut = NewsCdut.query.filter(NewsCdut.id > 300).all()
    user_said = Discuss.query.filter(Discuss.id > 1).all()
    today = get_today()
    return render_template('index.html', title='Home Page', news_cdut=news_cdut, today=today, user_said=user_said, discuss_form=discuss_form)


@bp.route('/add_discuss',  methods=['POST'])
@login_required
def add_discuss():
    data = json.loads(request.form.get('data'))
    username = data['username']
    said = data['said']
    # try catch return error
    discuss = Discuss(username=username, said=said)
    db.session.add(discuss)
    db.session.commit()
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


@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.identity = form.identity.data
        current_user.deadtime_info = form.deadtime_info.data
        current_user.deadtime_day = form.deadtime_day.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.identity.data = current_user.identity
        form.deadtime_info.data = current_user.deadtime_info
        form.deadtime_day.data = current_user.deadtime_day
    return render_template('edit_profile.html', title='Edit Profile', form=form)
