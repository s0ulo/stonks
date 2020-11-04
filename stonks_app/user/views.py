from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import (
    login_user,
    logout_user,
    current_user,
)
from sqlalchemy.exc import IntegrityError

from stonks_app.db import db
from stonks_app.user.forms import LoginForm, RegistrationForm
from stonks_app.user.models import User
from stonks_app.utils import get_redirect_target

blueprint = Blueprint("user", __name__, url_prefix="/")


@blueprint.route("/login")
def login():
    print(current_user)
    if current_user.is_authenticated:
        return redirect(get_redirect_target())
    title = "Authorization"
    login_form = LoginForm()
    return render_template("user/login.html", page_title=title, form=login_form)


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # flash("Authorization success!")
            return redirect(get_redirect_target())
    flash("Login or password not found!")
    return redirect(url_for("user.login"))


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for("user.login"))


@blueprint.route("/register")
def register():
    # print(current_user)
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    title = "Registration"
    form = RegistrationForm()
    return render_template(
        "user/registration.html", page_title=title, form=form
    )


@blueprint.route("/process-reg", methods=["POST"])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        stonks_user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            email=form.email.data,
            role="user",
        )
        stonks_user.set_password(form.password.data)
        db.session.add(stonks_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Registration failed. Username or e-mail already exists.")
            return redirect(url_for("user.register"))
        flash("Registration completed successfully.")
        return redirect(url_for("user.login"))
    flash("Registration failed. Please check registration form.")
    return redirect(url_for("user.register"))
