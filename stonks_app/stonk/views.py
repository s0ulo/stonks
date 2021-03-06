from flask import Blueprint, render_template
from flask_login import login_required
from stonks_app.stonk.models import StocksAttributes, Sectors, Countries
from stonks_app.db import db

import stonks_app.graph

blueprint = Blueprint("stonk", __name__)


@blueprint.route("/tickers")
@login_required
def tickers():
    """
    Tickers attributes table
    """
    tickers_info = (
        db.session.query(
            StocksAttributes.stock_name,
            StocksAttributes.ticker,
            StocksAttributes.stock_exchange_name,
            Sectors.sector_name,
            Countries.country,
        )
        .join(Sectors, StocksAttributes.sector_id == Sectors.id)
        .join(Countries, StocksAttributes.country_id == Countries.id)
        .all()
    )
    return render_template(
        "stonk/tickers.html",
        title="Tickers Information",
        description="This page shows all available ticker attributes just for lulz",
        # stock_attr_list=StocksAttributes.query.all()
        stock_attr_list=tickers_info,
    )


@blueprint.route("/tickers/<string:id>")
def plotlygraphs(id):
    ticker_name = (
        StocksAttributes.query.filter(StocksAttributes.ticker == id)
        .first()
        .stock_name
    )

    return render_template(
        "stonk/plotlygraphs.html",
        title=ticker_name + " high and low prices",
        ticker_name=ticker_name,
        scatter_plot=stonks_app.graph.historical_scatter(id),
        candle_plot=stonks_app.graph.historical_candle(id),
    )
