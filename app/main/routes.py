from datetime import datetime

from flask import render_template, flash, redirect, request, url_for, jsonify, json
from flask_login import current_user, login_required
import re
from app import db
from app.forms import DiscussForm
from app.main import bp
from app.models import User, Discuss, AnnounceModel
from app.news_cdut.models import NewsCdut
from app.spider.cdut import init_news
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
    news_cduts, all_count = init_news()
    news_cdut = news_cduts[-7:-1]
    notices = AnnounceModel.query.filter().order_by(AnnounceModel.up_time.desc()).limit(6)
    user_said = Discuss.query.filter(Discuss.id > 1).all()
    today = get_today()
    thisdate = datetime.now()
    thisdatetime = datetime.now()
    return render_template('index.html', title='Home Page', news_cdut=news_cdut, today=today, user_said=user_said, discuss_form=discuss_form, notices=notices, date=thisdate,datetime=thisdatetime,re=re)


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
    return jsonify({"success": 200, "user_said": [i.serialize() for i in user_said]})


@bp.route('/announce/more', methods=['GET', 'POST'])
def more():
    page = request.args.get('page', 1, type=int)
    announce_models = AnnounceModel.query.order_by(AnnounceModel.up_time.desc()).paginate(page, 10, False)
    next_url = url_for('news_cdut.more', page=announce_models.next_num) if announce_models.has_next else None
    prev_url = url_for('news_cdut.more', page=announce_models.prev_num) if announce_models.has_prev else None
    return render_template('announces/more.html', announces=announce_models.items, next_url=next_url, prev_url=prev_url)









