import requests
from stonks_app.datamodel import (
    db,
    HistoricalPrices,
    StocksAttributes,
    Peers,
    Countries,
    Sectors,
    Industries,
)  # импортируем модель данных
from stonks_app import create_app
from datetime import datetime
from top50_stocks import ticker_list  # импортируем список топ 50 компаний
from flask import current_app


# дергаем API с историческими ценами iex по конкретной акции,
# сохраняем ответ в локальную переменную,
# запускаем функцию сохранения в БД
# чтобы перейти из снадбокса в прод надо
# поменять УРЛ на https://cloud.iexapis.com/stable/stock/{ticker}/chart/1y
# поменять токен на SK_IEX_TOKEN
def get_historical_prices(tckr):
    hist_prices_url = \
        f'https://cloud.iexapis.com/stable/stock/{tckr}/chart/1y'
    params = {
        'token': current_app.config['SK_IEX_TOKEN']
    }
    data = requests.get(hist_prices_url, params=params)
    data.raise_for_status()
    data = data.json()
    store_hist_prices(tckr, data)


# функция сохранения в БД исторических цен.
# Для кажтого элемента списка, полученного в ответе из API
# берем небоходимые значение и кладем в БД.
# Дату приводим к соответствующему типу данных.
def store_hist_prices(tckr, data):
    for i in data:
        i["date"] = datetime.strptime(i["date"], "%Y-%m-%d")
        hist_prices = HistoricalPrices(
            ticker=tckr,
            date=i["date"],
            price_close=i["close"],
            price_open=i["open"],
            price_high=i["high"],
            price_low=i["low"],
            volume=i["volume"],
        )
        db.session.add(hist_prices)
        db.session.commit()


# дергаем апишку iex для получения информации по компании
# сохраняем ответ в локальную переменную,
# запускаем функцию сохранения в БД для сран, индустрий, секторов, атрибутов
# чтобы перейти из снадбокса в прод надо
# поменять УРЛ на https://cloud.iexapis.com/stable/stock/{tckr}/company
# поменять токен на SK_IEX_TOKEN
def get_rest_of_data(tckr):
    rest_of_data_url = \
        f'https://cloud.iexapis.com/stable/stock/{tckr}/company'
    params = {
        'token': current_app.config['SK_IEX_TOKEN']
    }
    data = requests.get(rest_of_data_url, params=params)
    data.raise_for_status()
    data = data.json()
    store_countries(data)
    store_industries(data)
    store_sectores(data)
    store_stock_attrs(tckr, data)


# сохранение атрибутов акций в БД
# в началае проверяем на дубликаты
# ID стран и секторов тянем из других таблиц
def store_stock_attrs(tckr, data):
    stock_exists = StocksAttributes.query.filter(
        StocksAttributes.ticker == tckr).count()
    if not stock_exists:
        stock_attrs = StocksAttributes(
            stock_name=data["companyName"],
            ticker=tckr,
            stock_exchange_name=data["exchange"],
            country_id=Countries.query.filter(
                Countries.country == data["country"]).first().id,
            sector_id=Sectors.query.filter(
                Sectors.sector_name == data["sector"]).first().id)
        db.session.add(stock_attrs)
        db.session.commit()


# сохранение индустрий в БД
# в началае проверяем на дубликаты
def store_industries(data):
    industry_exists = Industries.query.filter(
        Industries.industry_name == data["industry"]).count()
    if not industry_exists:
        indstr = Industries(industry_name=data["industry"])
        db.session.add(indstr)
        db.session.commit()


# сохранение секторов в БД
# в началае проверяем на дубликаты
# ID синдустрий тянем из других таблиц
def store_sectores(data):
    sector_exists = Sectors.query.filter(
        Sectors.sector_name == data["sector"]).count()
    if not sector_exists:
        sctrs = Sectors(
            sector_name=data["sector"],
            industry_id=Industries.query.filter(
                Industries.industry_name == data["industry"]).first().id)
        db.session.add(sctrs)
        db.session.commit()


# сохранение стран в БД
# в началае проверяем на дубликаты
def store_countries(data):
    country_exists = Countries.query.filter(
        Countries.country == data["country"]).count()
    if not country_exists:
        cntrs = Countries(country=data["country"])
        db.session.add(cntrs)
        db.session.commit()


# получаем пиры акций
# вызываем функцию сохранения в БД
# чтобы перейти из снадбокса в прод надо
# поменять УРЛ на https://cloud.iexapis.com/stable/stock/{tckr}/peers
# поменять токен на SK_IEX_TOKEN
def get_peers(tckr):
    peers_url = f'https://cloud.iexapis.com/stable/stock/{tckr}/peers'
    params = {
        'token': current_app.config['SK_IEX_TOKEN']
    }
    data = requests.get(peers_url, params=params)
    data.raise_for_status()
    data = data.json()
    store_peers(tckr, data)


# сохраняем пиры в БД
# итерируемся по словарю, который приходит в ответе
# проверяем, что тикер этого пира есть в таблице stock_attributes
# если есть - берем оттуда,
# если нет - вызываем полусение атрибутов для этого тикера
# и потом уже сохраняем
def store_peers(tckr, data):
    for i in data:
        peer_exists = StocksAttributes.query.filter(
            StocksAttributes.ticker == i).count()
        if peer_exists == 1:
            prs = Peers(ticker=tckr,
                peer_id=StocksAttributes.query.filter(
                    StocksAttributes.ticker == i).first().id)
            db.session.add(prs)
            db.session.commit()
        else:
            get_rest_of_data(i)
            prs = Peers(ticker=tckr,
                peer_id=StocksAttributes.query.filter(
                    StocksAttributes.ticker == i).first().id)
            db.session.add(prs)
            db.session.commit()


# запрос лимита сообщений в АПИ
# чтобы перейти из снадбокса в прод надо
# поменять УРЛ на https://cloud.iexapis.com/stable/account/metadata
# поменять токен на SK_IEX_TOKEN
def messages_left():
    metadata_url = 'https://cloud.iexapis.com/stable/account/metadata'
    params = {
        'token': current_app.config['SK_IEX_TOKEN']
    }
    messages = requests.get(metadata_url, params=params)
    messages = messages.json()
    messages_limit = int(messages['messageLimit'])
    return messages_limit


# запускаем скачивание данных.
# Итерируемся по импортированному списку ТОП 50 акций
# В консоль выводится счетчик оставшихся акций и лимит запросов
# если запросов осталось меньше, чем надо для
# скачивания полной инфы про 1 акцию - прерываем
app = create_app()
with app.app_context():

    tckrlst = ticker_list[1:]
    for t in tckrlst:
        stop = messages_left()
        if stop < 3100:
            break
        get_historical_prices(t)
        get_rest_of_data(t)
        countdown = len(ticker_list) - (ticker_list.index(t)) + 1
        print(
            f"{t} data saved, {str(countdown)} stonks remained, {stop} messages remained"
            )
