from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


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
