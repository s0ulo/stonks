"""Route declaration."""

from flask import current_app as app
from flask import render_template
from stonks_app.datamodel import StocksAttributes, HistoricalPrices
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import numpy as np
import pandas as pd

@app.route("/")
def home():
    """Landing page."""
    nav = [
        {"name": "Home", "url": "/"},
        {"name": "About", "url": "https://example.com/2"}
    ]

    return render_template(
        "home.html",
        nav=nav,
        title="Stonks First Steps Demo",
        description="Hello! I use page templates with Flask & Jinja.",
        stock_attr_list=StocksAttributes.query.all(),
    )

@app.route("/<string:id>")
def plotlygraphs(id):
    """Landing page."""
    nav = [
        {"name": "Home", "url": "/"},
        {"name": "About", "url": "https://example.com/2"}
    ]
    ticker_name = StocksAttributes.query.filter(StocksAttributes.ticker == id).first().stock_name

    return render_template(
        "plotlygraphs.html",
        nav=nav,
        title=ticker_name + ' high and low prices',
        ticker_name=ticker_name,
        plot=create_plot(id)
    )

def create_plot(ticker):
    df1 = pd.DataFrame(HistoricalPrices.query.filter(HistoricalPrices.ticker == ticker).with_entities(HistoricalPrices.date, HistoricalPrices.price_high))
    df2 = pd.DataFrame(HistoricalPrices.query.filter(HistoricalPrices.ticker == ticker).with_entities(HistoricalPrices.date, HistoricalPrices.price_low))

    data = [
        go.Scatter(
            x=df1["date"], 
            y=df1["price_high"],
            name='High ' + StocksAttributes.query.filter(StocksAttributes.ticker == ticker).first().stock_name
        ),
        go.Scatter(
            x=df2["date"], 
            y=df2["price_low"],
            name='Low ' + StocksAttributes.query.filter(StocksAttributes.ticker == ticker).first().stock_name
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON