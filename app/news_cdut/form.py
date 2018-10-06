from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    info = StringField('info', render_kw={"placeholder": "信息"})
    time = StringField('time', render_kw={"placeholder": "日期"})
    submit = SubmitField('search')

