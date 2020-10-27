from datetime import datetime
from flask_login import UserMixin
from stonks_app.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class HistoricalPrices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    price_close = db.Column(db.Float, nullable=False)
    price_open = db.Column(db.Float, nullable=True)
    price_high = db.Column(db.Float, nullable=True)
    price_low = db.Column(db.Float, nullable=True)
    volume = db.Column(db.Float, nullable=True)
    db.UniqueConstraint("ticker", "date")

    def __repr__(self):
        return (
            f"<historical_prices {self.date} {self.ticker} {self.price_close}>"
        )


class StocksAttributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String, unique=True, nullable=False)
    ticker = db.Column(db.String, unique=True, nullable=False)
    stock_exchange_name = db.Column(db.String, nullable=False)
    sector_id = db.Column(db.Integer, nullable=False)
    country_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<stock_attributes {self.stock_name} {self.ticker} {self.sector_id}>"


class Peers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, unique=True, nullable=False)
    peer_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<peers {self.ticker} {self.peer_id}>"


class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<countries {self.id} {self.country}>"


class Sectors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector_name = db.Column(db.String, unique=True, nullable=False)
    industry_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<sectors {self.id} {self.sector_name} {self.industry_id}>"


class Industries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry_name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<industries {self.industry_name}>"


class User(db.Model, UserMixin):
    """
    Database Model for Users
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

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
