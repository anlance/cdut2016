from datetime import datetime

from flask import render_template, flash, redirect, request, url_for, jsonify, json
from flask_login import current_user, login_required

from app import db
from app.forms import DiscussForm
from app.main import bp
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











