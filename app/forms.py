from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import Length


class DiscussForm(FlaskForm):
    username = StringField('username', render_kw={"hidden": "hidden"})
    said = TextAreaField('said', validators=[Length(min=0, max=140)], render_kw={"placeholder": "选择你的快乐", "maxlength": 50})
    # submit = SubmitField('发送')