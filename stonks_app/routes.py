"""Route declaration."""

from flask import current_app as app
from flask import render_template, flash, redirect, url_for
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)
from stonks_app.datamodel import StocksAttributes, User
from stonks_app.forms import LoginForm
import stonks_app.graph


@app.errorhandler(404)
def page_not_found(e):
    # set the 404 status explicitly
    return render_template("404.html"), 404


@app.route("/")
@login_required
def home():
    """Landing page."""

    return render_template(
        "home.html",
        title="Stonks First Steps Demo",
        description="Hello! I use page templates with Flask & Jinja.",
        stock_attr_list=StocksAttributes.query.all(),
    )


@app.route("/login")
def login():
    print(current_user)
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    title = "Authorization"
    login_form = LoginForm()
    return render_template("login.html", page_title=title, form=login_form)


@app.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # flash("Authorization success!")
            return redirect(url_for("home"))
    flash("Login or password not found!")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for("login"))


@app.route("/tickers")
@login_required
def tickers():
    """
    Tickers attributes table
    """

    return render_template(
        "tickers.html",
        title="Tickers Information",
        description="This page shows all available ticker attributes just for lulz",
        stock_attr_list=StocksAttributes.query.all(),
    )


@app.route("/tickers/<string:id>")
def plotlygraphs(id):
    ticker_name = (
        StocksAttributes.query.filter(StocksAttributes.ticker == id)
        .first()
        .stock_name
    )

    return render_template(
        "plotlygraphs.html",
        title=ticker_name + " high and low prices",
        ticker_name=ticker_name,
        scatter_plot=stonks_app.graph.historical_scatter(id),
        candle_plot=stonks_app.graph.historical_candle(id),
    )
