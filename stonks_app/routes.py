"""Route declaration."""

from flask import current_app as app
from flask import render_template


@app.route("/")
def home():
    """Landing page."""
    nav = [
        {"name": "Home", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        {"name": "About", "url": "https://example.com/2"},
    ]
    return render_template(
        "home.html",
        nav=nav,
        title="Stonks First Steps Demo",
        description="Hello! I use page templates with Flask & Jinja.",
    )
