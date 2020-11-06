"""Route declaration."""

from flask import current_app as app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    # set the 404 status explicitly
    return render_template("404.html"), 404


@app.route("/")
def home():
    """Landing page."""

    return render_template(
        "home.html",
        title="Stonks Apps Demo",
        description="Hello, everyone! This is Stonks Flask App!",
    )
