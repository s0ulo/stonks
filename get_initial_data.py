import requests
from sqlalchemy.exc import IntegrityError
from stonks_app.stonk.models import (
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


def get_from_api(tckr, extension):
    """
    Дергаем API, сохраняем ответ в `data`
    """
    global params, link_env
    api_url = f'https://{link_env}.iexapis.com/stable/stock/{tckr}/{extension}'
    data = requests.get(api_url, params=params)
    data.raise_for_status()
    data = data.json()
    return data


# дергаем API с историческими ценами iex по конкретной акции,
# сохраняем ответ в локальную переменную,
# запускаем функцию сохранения в БД
# чтобы перейти из снадбокса в прод надо
# поменять УРЛ на https://cloud.iexapis.com/stable/stock/{ticker}/chart/1y
# поменять токен на SK_IEX_TOKEN
def get_historical_prices(tckr):
    extension_for_url = 'chart/1y'
    historical_prices = get_from_api(tckr, extension_for_url)
    store_historical_prices(tckr, historical_prices)


# функция сохранения в БД исторических цен.
# Для кажтого элемента списка, полученного в ответе из API
# берем небоходимые значение и кладем в БД.
# Дату приводим к соответствующему типу данных.
def store_historical_prices(tckr, data):
    try:
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
    except (IntegrityError):
        db.session.rollback()


# дергаем апишку iex для получения информации по компании
# сохраняем ответ в локальную переменную,
# запускаем функцию сохранения в БД для сран, индустрий, секторов, атрибутов
# чтобы перейти из снадбокса в прод надо
# поменять УРЛ на https://cloud.iexapis.com/stable/stock/{tckr}/company
# поменять токен на SK_IEX_TOKEN
def get_rest_of_data(tckr):
    extension_for_url = 'company'
    rest_of_data = get_from_api(tckr, extension_for_url)
    store_countries(rest_of_data)
    store_industries(rest_of_data)
    store_sectores(rest_of_data)
    store_stock_attrs(tckr, rest_of_data)


# сохранение атрибутов акций в БД
# в началае проверяем на дубликаты
# ID стран и секторов тянем из других таблиц
def store_stock_attrs(tckr, data):
    # stock_exists = StocksAttributes.query.filter(
    #     StocksAttributes.ticker == tckr).count()
    # if not stock_exists:
    try:
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
    except (IntegrityError):
        db.session.rollback()


# сохранение индустрий в БД
# в началае проверяем на дубликаты
def store_industries(data):
    # industry_exists = Industries.query.filter(
    #     Industries.industry_name == data["industry"]).count()
    # if not industry_exists:
    try:
        indstr = Industries(industry_name=data["industry"])
        db.session.add(indstr)
        db.session.commit()
    except (IntegrityError):
        db.session.rollback()


# сохранение секторов в БД
# в началае проверяем на дубликаты
# ID синдустрий тянем из других таблиц
def store_sectores(data):
    # sector_exists = Sectors.query.filter(
    #     Sectors.sector_name == data["sector"]).count()
    # if not sector_exists:
    try:
        sctrs = Sectors(
            sector_name=data["sector"],
            industry_id=Industries.query.filter(
                Industries.industry_name == data["industry"]).first().id)
        db.session.add(sctrs)
        db.session.commit()
    except (IntegrityError):
        db.session.rollback()


# сохранение стран в БД
# в началае проверяем на дубликаты
def store_countries(data):
    # country_exists = Countries.query.filter(
    #     Countries.country == data["country"]).count()
    # if not country_exists:
    try:
        cntrs = Countries(country=data["country"])
        db.session.add(cntrs)
        db.session.commit()
    except (IntegrityError):
        db.session.rollback()


# получаем пиры акций
# вызываем функцию сохранения в БД
# чтобы перейти из снадбокса в прод надо
# поменять УРЛ на https://cloud.iexapis.com/stable/stock/{tckr}/peers
# поменять токен на SK_IEX_TOKEN
def get_peers(tckr):
    extension_for_url = 'peers'
    peers_data = get_from_api(tckr, extension_for_url)
    store_peers(tckr, peers_data)


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
            prs = Peers(
                ticker=tckr, peer_id=StocksAttributes.query.filter(
                    StocksAttributes.ticker == i).first().id)
            db.session.add(prs)
            db.session.commit()
        else:
            get_rest_of_data(i)
            prs = Peers(
                ticker=tckr, peer_id=StocksAttributes.query.filter(
                    StocksAttributes.ticker == i).first().id
            )
            db.session.add(prs)
            db.session.commit()


# запрос лимита сообщений в АПИ
# чтобы перейти из снадбокса в прод надо
# поменять УРЛ на https://cloud.iexapis.com/stable/account/metadata
# поменять токен на SK_IEX_TOKEN
def is_limit_exceeded():
    global params, link_env
    metadata_url = f'https://{link_env}.iexapis.com/stable/account/metadata'
    messages = requests.get(metadata_url, params=params).json()
    messages_left = int(messages['messageLimit']) \
        - int(messages['messagesUsed'])
    if messages_left < current_app.config['MESSAGES_FOR_1_TICKER']:
        return True
    return False


def limit_exceeded():
    global params, link_env
    metadata_url = f'https://{link_env}.iexapis.com/stable/account/metadata'
    messages = requests.get(metadata_url, params=params).json()
    messages_left = int(messages['messageLimit']) \
        - int(messages['messagesUsed'])
    return messages_left


# запускаем скачивание данных.
# Итерируемся по импортированному списку ТОП 50 акций
# В консоль выводится счетчик оставшихся акций и лимит запросов
# если запросов осталось меньше, чем надо для
# скачивания полной инфы про 1 акцию - прерываем
app = create_app()
with app.app_context():

    link_env = 'cloud'
    params = {
        'token': current_app.config['SK_IEX_TOKEN1']
    }
    tckrlst = ticker_list[19:]
    for ticker in tckrlst:
        if is_limit_exceeded():
            countdown_messages = limit_exceeded()
            print(
                f'Превышен лимит запросов, осталось {str(countdown_messages)}'
                )
            break
        get_historical_prices(ticker)
        get_rest_of_data(ticker)
        countdown_tickers = len(ticker_list) - (ticker_list.index(ticker)) + 1
        countdown_messages = limit_exceeded()
        print(
            f"""{ticker} data saved,
                {str(countdown_tickers)} stonks remained,
                {str(countdown_messages)} messages remained.
                """)
