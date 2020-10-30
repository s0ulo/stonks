from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired
import email_validator


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control py-4",
            "placeholder": "Enter username",
        },
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control py-4",
            "placeholder": "Enter password",
        },
    )
    submit = SubmitField("Login", render_kw={"class": "btn btn-primary"})

    remember_me = BooleanField(
        "Stay signed in", default=True, render_kw={"class": "form-check-input"}
    )


class RegistrationForm(FlaskForm):
    firstname = StringField(
        "First Name",
        render_kw={
            "class": "form-control py-4",
            "placeholder": "Enter First Name",
        },
    )
    lastname = StringField(
        "Last Name",
        render_kw={
            "class": "form-control py-4",
            "placeholder": "Enter Last Name",
        },
    )
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control py-4",
            "placeholder": "Enter username",
        },
    )
    email = StringField(
        "E-mail",
        validators=[DataRequired(), Email()],
        render_kw={
            "class": "form-control py-4",
            "placeholder": "Enter e-mail",
        },
    )    
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control py-4",
            "placeholder": "Enter password",
        },
    )
    password2 = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo('password')],
        render_kw={
            "class": "form-control py-4",
            "placeholder": "Confirm password",
        },
    )    
    submit = SubmitField("Register", render_kw={"class": "btn btn-primary"})
