import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller


def find_d(df_column, p_value_threshold=0.05):
    if adfuller(df_column)[1] < p_value_threshold:
        d = 0
    elif adfuller(df_column.diff().dropna())[1] < p_value_threshold:
        d = 1
    else:
        d = 2
    return d


def arima_forecast(trends_time_series, forecast_intervals, p=3, q=3):
    df = pd.DataFrame(trends_time_series)
    important_topics = []
    for c in df.columns:
        d = find_d(df[c])
        arima_model = ARIMA(df[c], order=(p, d, q))
        model = arima_model.fit()
        forecast = model.forecast(forecast_intervals).to_list()
        forecast = [round(f,2) for f in forecast]
        important_topics.append((c, max(forecast)))
        trends_time_series[c].extend(forecast)
    important_topics.sort(key=lambda x: x[1], reverse=True)
    important_topics = [important_topics[0][0], important_topics[1][0]]
    return trends_time_series, important_topics
