"""Route declaration."""

from flask import current_app as app
from flask import render_template
from stonks_app.datamodel import db, Stocks_attributes, Historical_prices
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
        stock_attr_list=Stocks_attributes.query.all(),
    )

@app.route("/<string:id>")
def plotlygraphs(id):
    """Landing page."""
    nav = [
        {"name": "Home", "url": "/"},
        {"name": "About", "url": "https://example.com/2"}
    ]
    ticker_name = Stocks_attributes.query.filter(Stocks_attributes.ticker == id).first().stock_name

    return render_template(
        "plotlygraphs.html",
        nav=nav,
        title=ticker_name + ' high and low prices',
        ticker_name=ticker_name,
        plot=create_plot(id)
    )

def create_plot(ticker):
    df1 = pd.DataFrame(Historical_prices.query.filter(Historical_prices.ticker == ticker).with_entities(Historical_prices.date, Historical_prices.price_high))
    df2 = pd.DataFrame(Historical_prices.query.filter(Historical_prices.ticker == ticker).with_entities(Historical_prices.date, Historical_prices.price_low))

    data = [
        go.Scatter(
            x=df1["date"], 
            y=df1["price_high"],
            name='High ' + Stocks_attributes.query.filter(Stocks_attributes.ticker == ticker).first().stock_name
        ),
        go.Scatter(
            x=df2["date"], 
            y=df2["price_low"],
            name='Low ' + Stocks_attributes.query.filter(Stocks_attributes.ticker == ticker).first().stock_name
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON