import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import numpy as np


def find_d(df_column, p_value_threshold=0.05):
    if adfuller(df_column)[1] < p_value_threshold:
        d = 0
    elif adfuller(df_column.diff().dropna())[1] < p_value_threshold:
        d = 1
    else:
        d = 2
    return d


def mean_abstract_error(a, b):
    l = len(a)
    s = 0
    for i in range(l):
        s+=abs(a[i]-b[i])
    return s/l


def arima_forecast(trends_time_series, forecast_intervals, p=3, q=3):
    df = pd.DataFrame(trends_time_series)
    important_topics, train_loss, val_loss = [], [], []
    for c in df.columns:
        train_set = df[c][:-forecast_intervals]
        d = find_d(train_set)

        arima_model = ARIMA(train_set, order=(p, d, q))
        model = arima_model.fit()

        predictions = model.predict().to_list()
        train_loss.append(mean_abstract_error(predictions, train_set.to_list()))

        forecast = model.forecast(2*forecast_intervals).to_list()
        val_loss.append(mean_abstract_error(forecast[:forecast_intervals], df[c][-forecast_intervals:].to_list()))
        forecast = [round(f,2) for f in forecast]

        important_topics.append((c, max(forecast)))
        trends_time_series[c] = trends_time_series[c][:-forecast_intervals]
        trends_time_series[c].extend(forecast)

    important_topics.sort(key=lambda x: x[1], reverse=True)
    important_topics = [important_topics[0][0], important_topics[1][0]]
    important_topics = important_topics[0].split('_') + important_topics[1].split('_')
    important_topics = ' _ '.join(important_topics)

    return trends_time_series, important_topics, train_loss, val_loss


def find_best_arima(trends_time_series, forecast_intervals):
    results = {}
    min_train = 10000
    min_val = 10000
    print('start to find best arima:')
    for p in range(10):
        for q in range(10):
            df = pd.DataFrame(trends_time_series)
            important_topics, train_loss, val_loss = [], [], []
            for c in df.columns:
                train_set = df[c][:-forecast_intervals]
                d = find_d(train_set)

                arima_model = ARIMA(train_set, order=(p, d, q))
                model = arima_model.fit()

                predictions = model.predict().to_list()
                train_loss.append(mean_abstract_error(predictions, train_set.to_list()))

                forecast = model.forecast(2 * forecast_intervals).to_list()
                val_loss.append(
                    mean_abstract_error(forecast[:forecast_intervals], df[c][-forecast_intervals:].to_list()))

            results[str(p)+','+str(q)] = (np.average(train_loss), np.average(val_loss))
            if min_val>np.average(val_loss):
                min_pq_val = (p,q)
                min_val = np.average(val_loss)
            if min_train>np.average(train_loss):
                min_pq_train = (p,q)
                min_train = np.average(train_loss)
            print(results[str(p)+','+str(q)])

    print('best for train:', min_pq_train)
    print('best for val:', min_pq_val)
