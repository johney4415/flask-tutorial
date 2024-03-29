from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User

class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=20)])
    confirm = PasswordField('Request Password', validators=[DataRequired(), EqualTo('password')])
    # recaptcha =RecaptchaField()
    submit = SubmitField('註冊')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already used, please choose other one')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=20)])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign In')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('email not exists')


class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=20)])
    confirm = PasswordField('Request Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class PostTweetForm(FlaskForm):
    text = TextAreaField('Say Something...', validators=[DataRequired(),Length(min=1,max=140)])
    sumit = SubmitField('Post Text')