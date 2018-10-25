from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired()])
    about_me = TextAreaField('签名', validators=[Length(min=0, max=140)])
    identity = StringField('身份证号')
    school_number = StringField('学号')
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class DeadtimeForm(FlaskForm):
    deadtime_info = StringField('事件', validators=[DataRequired()])
    deadtime_day = DateField('时间', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(DeadtimeForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
