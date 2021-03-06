__version__ = "0.2.0"

"""Initialize Flask Application."""
from flask import Flask, redirect
from flask.helpers import url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from stonks_app.db import db
from stonks_app.user.models import User
from stonks_app.user.views import blueprint as user_blueprint
from stonks_app.stonk.views import blueprint as stonk_blueprint


def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder="templates")
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)

    # Add and init LoginManager instance
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # Add Blueprints
    app.register_blueprint(user_blueprint)
    app.register_blueprint(stonk_blueprint)

    with app.app_context():

        from . import routes

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

        @login_manager.unauthorized_handler
        def unauthorized_callback():
            return redirect(url_for('user.login'))

        # render_as_batch for renaming columns in SQLite
        if db.engine.url.drivername == "sqlite":
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)

        return app
