from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(max=30)])
    password = StringField('Password', validators=[InputRequired()], widget=PasswordInput(hide_value=False))
    submit = SubmitField('Login')
