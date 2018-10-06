import re
from datetime import datetime
from app import db, create_app
from app.models import NewsConfig
from app.news_cdut.models import NewsCdut
from app.spider.cdut import init_news, update_news

app = create_app()
app.app_context().push()


def init_config():
    news_config = NewsConfig(id=1, cdut_total=1, cdut_page_n=10)
    with app.app_context():
        db.session.add(news_config)
        db.session.commit()


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
    news_config = NewsConfig.query.filter_by(id=1).first()
    news_config.cdut_total = cur_total
    db.session.commit()
    save_to_db(news)
    print('-init-cdut-')


def update_cdut():
    cdut_totals = NewsConfig.query.filter_by(id=1).first()
    print('--2222---')
    print(int(cdut_totals.cdut_total))
    news = update_news(int(cdut_totals.cdut_total))
    if len(news) != 0:
        save_to_db(news)
    print('-update-cdut-')


def init():
    # 初始化db存储的配置信息
    init_config()
    init_news()
