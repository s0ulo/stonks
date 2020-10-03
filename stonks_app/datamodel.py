from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class historical_prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    price_close = db.Column(db.Float, nullable=False)
    price_open = db.Column(db.Float, nullable=True)
    price_high = db.Column(db.Float, nullable=True)
    price_low = db.Column(db.Float, nullable=True)
    price_volume = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return '<historical_prices {} {} {}>'.format(self.ticker, self.date, self.price_close)


class stocks_attributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String, unique=True, nullable=False)
    ticker = db.Column(db.String, unique=True, nullable=False)
    stock_exchange_name = db.Column(db.String, unique=True, nullable=False)
    sector_id = db.Column(db.Integer, unique=True, nullable=False)
    country_id = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<stock_attributes {} {}>'.format(self.stock_name, self.ticker)


class peers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    peer_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<peers {} {}>'.format(self.ticker, self.peer_id)


class countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<countries {}>'.format(self.country)


class sectors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector_name = db.Column(db.String, nullable=False)
    industry_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<sectors {} {}>'.format(self.sector_name, self.industry_id)


class industries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<industries {}>'.format(self.industry_name)
