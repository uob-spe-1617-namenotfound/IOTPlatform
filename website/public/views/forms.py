from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import InputRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    email_address = StringField(
        'Email',
        validators=[InputRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired()]
    )
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email_address = StringField(
        'Email',
        validators=[InputRequired(), Email(), Length(min=3, max=50)]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=25)]
    )
    password_repeat = PasswordField(
        'Repeat Password',
        validators=[InputRequired(), EqualTo('password',
                                             message='Passwords must match.')]
    )
    name = StringField(
        'Name',
        validators=[InputRequired(), Length(min=2, max=60)]
    )

    submit = SubmitField('Register')
