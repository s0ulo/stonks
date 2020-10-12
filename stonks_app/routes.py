"""Route declaration."""

from flask import current_app as app
from flask import render_template
from stonks_app.datamodel import StocksAttributes
import stonks_app.graph


@app.errorhandler(404)
def page_not_found(e):
    # set the 404 status explicitly
    return render_template('404.html'), 404


@app.route("/")
def home():
    """Landing page."""

    return render_template(
        "home.html",
        title="Stonks First Steps Demo",
        description="Hello! I use page templates with Flask & Jinja.",
        stock_attr_list=StocksAttributes.query.all(),
    )


@app.route("/tickers")
def tickers():
    """
    Tickers attributes table
    """

    return render_template(
        "tickers.html",
        title="Tickers Information",
        description="This page shows all available ticker attributes just for lulz",
        stock_attr_list=StocksAttributes.query.all(),
    )


@app.route("/tickers/<string:id>")
def plotlygraphs(id):
    ticker_name = StocksAttributes.query.filter(
        StocksAttributes.ticker == id).first().stock_name

    return render_template(
        "plotlygraphs.html",
        title=ticker_name + ' high and low prices',
        ticker_name=ticker_name,
        scatter_plot=stonks_app.graph.historical_scatter(id),
        candle_plot=stonks_app.graph.historical_candle(id)
    )
