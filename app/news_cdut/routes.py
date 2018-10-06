from flask import render_template, current_app, request, url_for, redirect, flash
from flask_login import login_required
from sqlalchemy import and_

from app.news_cdut import bp
from app.news_cdut.form import SearchForm
from app.news_cdut.models import NewsCdut


@login_required
@bp.route('/news_cdut/more', methods=['GET', 'POST'])
def more():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        info = form.info.data
        time = form.time.data
        news_cdut = NewsCdut.query.filter(and_(NewsCdut.info.like("%"+info+"%"), NewsCdut.time.like("%"+time+"%")))\
            .order_by(NewsCdut.time.desc()).paginate(page, current_app.config['NEWS_PER_PAGE'], False)
        next_url = url_for('news_cdut.more', page=news_cdut.next_num) if news_cdut.has_next else None
        prev_url = url_for('news_cdut.more', page=news_cdut.prev_num) if news_cdut.has_prev else None

        # 获取检索到的所有条数
        temp = news_cdut
        num_news = len(temp.items)
        while temp.has_next:
            temp = temp.next()
            num_news += len(temp.items)
        num_page = num_news//10+int(1)
        if num_news == 0:
            num_page = 0
        if news_cdut:
            flash('共检索到'+str(num_news)+'条('+str(num_page)+'页)数据')
            return render_template('news_cdut/more.html', news_cdut=news_cdut.items, next_url=next_url,
                                   prev_url=prev_url, form=form)
        return redirect(url_for('news_cdut.more'))
    elif request.method == 'GET':
        news_cdut = NewsCdut.query.order_by(NewsCdut.time.desc()).paginate(page, current_app.config['NEWS_PER_PAGE'], False)
        next_url = url_for('news_cdut.more', page=news_cdut.next_num) if news_cdut.has_next else None
        prev_url = url_for('news_cdut.more', page=news_cdut.prev_num) if news_cdut.has_prev else None
        return render_template('news_cdut/more.html', news_cdut=news_cdut.items, next_url=next_url, prev_url=prev_url, form=form)


