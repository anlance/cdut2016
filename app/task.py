import re
import time
from datetime import datetime
from app import db, create_app
from app.auth.email import send_score_update_email
from app.models import User, Score
from app.news_cdut.models import NewsCdut
from app.spider.cdut import init_news
from app.spider.score import login_cdut, parse_stu_score

app = create_app()


def save_to_db(news):
    for item in news:
        days = re.sub('\D', '-', item[2]).rstrip('-')
        day = datetime.strptime(days, "%Y-%m-%d")
        news_cdut = NewsCdut(origin_url=item[0], info=item[1], time=day)
        with app.app_context():
            db.session.add(news_cdut)
            db.session.commit()


def init_cdut():
    app.app_context().push()
    news_cdut = NewsCdut.query.filter().order_by(NewsCdut.time.desc())
    for news in news_cdut:
        db.session.delete(news)
        db.session.commit()
    news, cur_total = init_news()
    save_to_db(news)
    print('init_success')


def init():
    print('--init_db--')
    db.drop_all(app=app)
    db.create_all(app=app)
    print('--init_cdut--')
    init_cdut()


def update_score():
    app.app_context().push()
    users = User.query.filter().all()
    print(datetime.now())
    for user in users:
        up_score_list = []
        if user.school_number and user.identity:
            response_obj, status = login_cdut(user.school_number, user.identity)
            score_list = parse_stu_score(response_obj, status)
            if len(score_list) > user.score_num:
                i = 0
                new_num = len(score_list) - user.score_num
                while i < new_num:
                    score = Score(user_id=user.id, term=score_list[i][0], name=score_list[i][1], teacher=score_list[i][2], credit=score_list[i][3], grade=score_list[i][4], type=score_list[i][5], gpa=score_list[i][6], up_time=score_list[i][7])
                    db.session.add(score)
                    up_score_list.append(score)
                    print(score)
                    i += 1
                send_score_update_email(user, up_score_list)
            user.score_num = len(score_list)
        db.session.commit()


