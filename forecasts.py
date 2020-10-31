import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from datetime import datetime
from stonks_app import create_app
from sqlalchemy.exc import IntegrityError
from stonks_app.datamodel import (
    FcstModel, db,
    HistoricalPrices,
    StocksAttributes,
    Forecast,
)  # импортируем модель данных


# Читаем данные из БД и сладываем их в датафрем
# Меняем названия колонок на такие как базе
# Кастуем колонку дата в тип даты
def create_dataframe(ticker):
    df = HistoricalPrices.query.filter(HistoricalPrices.ticker == ticker).with_entities(
        HistoricalPrices.ticker,
        HistoricalPrices.id,
        HistoricalPrices.date,
        HistoricalPrices.price_close).all()
    df = pd.DataFrame(df)
    names = {
        0: 'id',
        1: 'ticker',
        2: 'date',
        3: 'price_close',
        4: 'price_open',
        5: 'price_high',
        6: 'price_low',
        7: 'volume'
        }
    df.rename(columns=names, inplace=True)
    df['date'] = pd.to_datetime(df.date)
    df['date'] = df['date'].dt.strftime('%d/%m/%Y')
    return(df)


class PrepareDataset:
    '''Класс, который подготавливает датасет.

    Аргументы:
    df - датафрейм (ожидается что придет структура как из нашей БД);
    train_len - float от 0 до 1, какая часть данных идет в обучение;

    Атрибуты:
    train_data - обучение, numpy.ndarray;
    test_data - тест, numpy.ndarray.
    df - датафрейм, полученный на вход;
    train_len - float от 0 до 1, какая часть данных идет в обучение;
    test_len - float от 0 до 1, какая часть данных идет в тест.'''

    def __init__(self, df, train_len):
        self.train_len = train_len
        self.test_len = 1 - train_len
        self.df = df
        self.train_data = df[0:int(len(df)*train_len)]
        self.test_data = df[int(len(df)*train_len):]
        self.train_data = self.train_data['price_close'].values
        self.test_data = self.test_data['price_close'].values


def merge_fcst_with_ds(dataset, predictor):
    predictions = getattr(predictor, 'predictions')
    fcst = []
    for i in predictions:
        var = float(i)
        fcst.append(var)
    dataf = getattr(dataset, 'df')
    train_len = getattr(dataset, 'train_len')
    length = int(len(dataf)*train_len)
    df_fcst = dataf[length:]
    df_fcst.insert(len(df_fcst.columns), 'forecast_price', fcst, False)
    return(df_fcst)


class PredictorARIMA:
    def __init__(self, train, test, p, d, q):
        self.model_name = 'ARIMA'
        self.train = train
        self.test = test
        self.p = p
        self.d = d
        self.q = q
        self.predictions = []
        self.fcstdate = None
        self.mse = None

    def get(self):
        self.predictions = []
        self.fcstdate = datetime.now()
        history = [x for x in self.train]
        N_test_observations = len(self.test)
        order = (self.p, self.d, self.q)
        for time_point in range(N_test_observations):
            model = ARIMA(history, order=order)
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            self.predictions.append(yhat)
            true_test_value = self.test[time_point]
            history.append(true_test_value)
        self.mse = mean_squared_error(self.test, self.predictions)


def store_model(model, tckr):
    model_name = getattr(model, 'model_name')
    arima_p = getattr(model, 'p')
    arima_d = getattr(model, 'd')
    arima_q = getattr(model, 'q')
    date_created = getattr(model, 'fcstdate')
    mse = getattr(model, 'mse')
    try:
        mdl = FcstModel(
            ticker=tckr,
            model_name=model_name,
            arima_p=arima_p,
            arima_d=arima_d,
            arima_q=arima_q,
            date_created=date_created,
            mse=mse
        )
        db.session.add(mdl)
        db.session.commit()
        print('Model succesfully stored')
    except (IntegrityError):
        db.session.rollback()
        print('Model not stored')


def store_fcst(dataset, predictor):
    try:
        forecast_date1 = getattr(predictor, 'fcstdate')
        model_id1 = FcstModel.query.filter(FcstModel.date_created == forecast_date1).first().id
        for index, row in dataset.iterrows():
            fcsts = Forecast(
                ticker=row['ticker'],
                date=datetime.strptime(row['date'], "%d/%m/%Y"),
                forecast_price=row['forecast_price'],
                forecast_date=forecast_date1,
                model_id=model_id1
            )
            db.session.add(fcsts)
            db.session.commit()
    except (IntegrityError):
        db.session.rollback()
        print('Forecast not stored')


app = create_app()
with app.app_context():
    all_tickers_tuple = StocksAttributes.query.filter(StocksAttributes.ticker != 0).with_entities(StocksAttributes.ticker).all()
    fcstd_tickers_tuple = FcstModel.query.filter(FcstModel.ticker != 0).with_entities(FcstModel.ticker).all()
    all_tickers_list = []
    fcstd_tickers_list = []
    for t in all_tickers_tuple:
        a = str(t[0])
        all_tickers_list.append(a)
    for t in fcstd_tickers_tuple:
        a = str(t[0])
        fcstd_tickers_list.append(a)
    tickers_for_fcst = list(set(all_tickers_list) - set(fcstd_tickers_list))
    for t in tickers_for_fcst:
        print(f'starting forecasting for {t}')
        df = create_dataframe(t)
        ds = PrepareDataset(df, 0.7)
        fcst_model = PredictorARIMA(ds.train_data, ds.test_data, 1, 0, 0)
        predictions = fcst_model.get()
        store_model(fcst_model, t)
        ds_with_date = merge_fcst_with_ds(ds, fcst_model)
        store_fcst(ds_with_date, fcst_model)
        print(f'Forecast for {t} succesfully stored')
