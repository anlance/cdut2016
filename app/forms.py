from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.validators import Length


# 留言表单
class DiscussForm(FlaskForm):
    username = StringField('username', render_kw={"hidden": "hidden"})
    said = TextAreaField('said', validators=[Length(min=0, max=140)], render_kw={"placeholder": "留下您的宝贵建议", "maxlength": 50})
