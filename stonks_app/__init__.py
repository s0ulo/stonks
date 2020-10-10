__version__ = "0.1.0"

"""Initialize Flask Application."""
from flask import Flask
from stonks_app.datamodel import db


def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder="templates")
    app.config.from_pyfile("config.py")
    db.init_app(app)

    with app.app_context():
        from . import routes

        return app
