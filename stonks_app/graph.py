from stonks_app.stonk.models import StocksAttributes, HistoricalPrices
import json
import pandas as pd
import plotly
import plotly.graph_objs as go


def historical_scatter(ticker):
    price_high_df = pd.DataFrame(
        HistoricalPrices.query.filter(HistoricalPrices.ticker == ticker)
        .with_entities(HistoricalPrices.date, HistoricalPrices.price_high))

    price_low_df = pd.DataFrame(
        HistoricalPrices.query.filter(HistoricalPrices.ticker == ticker)
        .with_entities(HistoricalPrices.date, HistoricalPrices.price_low))

    data = [
        go.Scatter(
            x=price_high_df["date"], 
            y=price_high_df["price_high"],
            name='High ' + StocksAttributes.query.filter(
                StocksAttributes.ticker == ticker).first().stock_name
        ),
        go.Scatter(
            x=price_low_df["date"], 
            y=price_low_df["price_low"],
            name='Low ' + StocksAttributes.query.filter(
                StocksAttributes.ticker == ticker).first().stock_name
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def historical_candle(ticker):
    df = pd.DataFrame(
        HistoricalPrices.query.filter(HistoricalPrices.ticker == ticker).with_entities(HistoricalPrices.date, HistoricalPrices.price_low, HistoricalPrices.price_close, HistoricalPrices.price_high, HistoricalPrices.price_open))

    data = [
        go.Candlestick(
            x=df['date'],
            open=df['price_open'],
            high=df['price_high'],
            low=df['price_low'],
            close=df['price_close']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
