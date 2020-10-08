from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Historical_prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    price_close = db.Column(db.Float, nullable=False)
    price_open = db.Column(db.Float, nullable=True)
    price_high = db.Column(db.Float, nullable=True)
    price_low = db.Column(db.Float, nullable=True)
    volume = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<historical_prices {self.date} {self.ticker} {self.price_close}>"


class Stocks_attributes(db.Model):
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
    ticker = db.Column(db.String, nullable=False)
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
    sector_name = db.Column(db.String, nullable=False)
    industry_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<sectors {self.id} {self.sector_name} {self.industry_id}>"


class Industries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<industries {self.industry_name}>"
