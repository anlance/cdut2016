import re
from datetime import datetime
from app import db, create_app
from app.news_cdut.models import NewsCdut
from app.spider.cdut import init_news, update_news

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
    print('--init_cdut--')


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
    db.drop_all(app=app)
    db.create_all(app=app)
    print('--init_db--')
    init_cdut()
