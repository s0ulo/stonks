"""Route declaration."""

from flask import current_app as app
from flask import render_template
from flask_login import login_required
from stonks_app.stonk.models import StocksAttributes


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
