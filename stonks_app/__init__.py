__version__ = "0.1.0"

"""Initialize Flask Application."""
from flask import Flask


def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder="templates")

    with app.app_context():
        from . import routes

        return app
