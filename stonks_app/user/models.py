from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from stonks_app.db import db


class User(db.Model, UserMixin):
    """
    Database Model for Users
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    email = db.Column(db.String(50), index=True, unique=True)
    firstname = db.Column(db.String(50), index=True)
    lastname = db.Column(db.String(50), index=True)

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<Username: {self.username} | ID: {self.id}>"

    def set_password(self, password):
        """
        Sets password for each user and generates password hash via werkzeug. \n
        Hash is saved to `password` class attribute.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks provided password with hash in database. \n
        Returns True or False
        """
        return check_password_hash(self.password_hash, password)


class Favourite(db.Model):
    """
    Database Model for Users and their personal favourite stonks
    """
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(
        db.Integer, db.ForeignKey("stocks_attributes.id", ondelete="CASCADE"), index=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), index=True
    )

    ticker = relationship("StocksAttributes", backref="favourites")
    user = relationship("User", backref="favourites")

    def __repr__(self):
        return (
            f"<Favourites pair: User {self.user_id} - Ticker {self.stock_id} >"
        )
