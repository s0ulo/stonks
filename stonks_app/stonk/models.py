from stonks_app.db import db


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
        return f"""<stock_attributes
             {self.stock_name} {self.ticker} {self.sector_id}>"""


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


class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    forecast_date = db.Column(db.DateTime, nullable=False)
    forecast_price = db.Column(db.Float, nullable=False)
    model_id = db.Column(db.Integer, nullable=False)
    db.UniqueConstraint("ticker", "date", "model_id")

    __tablename__ = 'forecasts'

    def __repr__(self):
        return f"""<Forecasted price for {self.ticker}
             from {self.forecast_date} to {self.date}
             was {self.forecast_price}>"""


class FcstModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False)
    model_name = db.Column(db.String, nullable=False)
    arima_p = db.Column(db.Integer, nullable=True)
    arima_d = db.Column(db.Integer, nullable=True)
    arima_q = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)
    mse = db.Column(db.Float, nullable=False)

    __tablename__ = 'fcst_models'

    def __repr__(self):
        return f"""<Model {self.model_name},
             created {self.date_created}, MSE={self.mse}>"""
