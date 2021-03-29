from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField, RadioField
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import EmailField, DateTimeField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TrainForm(FlaskForm):
    sostav = RadioField('состав', choices=[('Y', 'младший'), ('O', 'старший')], default='Y',
                        validators=[DataRequired()])
    dur = IntegerField('Duration', validators=[DataRequired()])
    date = DateTimeField('Date', format='%Y-%m-%d', default=datetime.now())
    time = DateTimeField('Time', format='%H:%M', default=datetime.now().time())
    submit = SubmitField('Submit')


class DelTrain(FlaskForm):
    train_id = IntegerField('№ тренировки', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ZayavkaForm(FlaskForm):
    sostav = RadioField('состав', choices=[('Y', 'младший'), ('O', 'старший'), ('P', 'преподаватели')], default='Y',
                        validators=[DataRequired()])
    podgotovka = RadioField('ваш уровень подготовки',
                            choices=[('профи', 'профи'), ('любитель', 'любитель'), ('начинающий', 'начинающий')],
                            validators=[DataRequired()])
    about = StringField('немного о себе')
    submit = SubmitField('Submit')


class ProsmotrForm(FlaskForm):
    opin = RadioField('Что решаем', choices=[(True, 'принимаем'), (False, 'отклоняем')], default=False,
                      validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddNewsForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    img = FileField('image')
    submit = SubmitField('Submit')
