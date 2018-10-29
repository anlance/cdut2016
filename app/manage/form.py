from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class ToWriteForm(FlaskForm):
    name = StringField('公告标题', validators=[DataRequired()])
    info = TextAreaField('公告内容', validators=[DataRequired()])
    item_num = IntegerField('表格数目', validators=[DataRequired(), NumberRange(0, 20)])
    submit = SubmitField('准备发布')


class OneItemForm(FlaskForm):
    itname = StringField('字段名', validators=[DataRequired()])
    placeholder = StringField('示例', validators=[DataRequired()])


class TableForm(FlaskForm):
    items = FieldList(FormField(OneItemForm), min_entries=0, max_entries=20)
    submit = SubmitField('发布')


class OneAnnForm(FlaskForm):
    item = StringField('字段名', validators=[DataRequired()])


class SubmitForm(FlaskForm):
    items = FieldList(FormField(OneAnnForm), min_entries=0, max_entries=20)
    submit = SubmitField('提交')