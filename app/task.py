import re
from datetime import datetime, time
from app import db, create_app
from app.auth.email import send_score_update_email
from app.models import User, Score
from app.news_cdut.models import NewsCdut
from app.spider.cdut import init_news, update_news
from app.spider.score import login_cdut, parse_stu_score

app = create_app()


def save_to_db(news):
    url_head = 'http://www.aao.cdut.edu.cn/i'
    for item in news:
        days = re.sub('\D', '-', item[2]).rstrip('-')
        url_tail = item[0]
        url = url_head + url_tail.split('i')[-1]
        day = datetime.strptime(days, "%Y-%m-%d")
        news_cdut = NewsCdut(origin_url=url, info=item[1], time=day)
        with app.app_context():
            db.session.add(news_cdut)
            db.session.commit()


def init_cdut():
    news, cur_total = init_news()
    save_to_db(news)


def update_cdut():
    app.app_context().push()
    news_cdut = NewsCdut.query.filter().all()
    num = len(news_cdut)
    news = update_news(num)
    if len(news) != 0:
        save_to_db(news)
        print('--update_cdut--')
        print(datetime.now())
    print('--no_update_cdut--')


def init():
    print('--init_db--')
    db.drop_all(app=app)
    db.create_all(app=app)
    print('--init_cdut--')
    init_cdut()


def update_score():
    app.app_context().push()
    users = User.query.filter().all()
    for user in users:
        time.sleep(60)
        up_score_list = []
        if user.school_number and user.identity:
            response_obj, status = login_cdut(user.school_number, user.identity)
            score_list = parse_stu_score(response_obj, status)
            if len(score_list) > user.score_num:
                i = 0
                new_num = len(score_list) - user.score_num
                while i < new_num:
                    score = Score(user_id=user.id, term=score_list[i][0], name=score_list[i][1], teacher=score_list[i][2], credit=score_list[i][3], grade=score_list[i][4], type=score_list[i][5], gpa=score_list[i][6], up_time=score_list[i][7])
                    # db.session.add(score)
                    up_score_list.append(score)
                    print(score)
                    i += 1
                send_score_update_email(user, up_score_list)
            user.score_num = len(score_list)
        db.session.commit()

