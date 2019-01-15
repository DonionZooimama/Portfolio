import time
import warnings
import numpy as np
from numpy import newaxis
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import matplotlib.pyplot as plt
import sys
import pandas as pd

sys.path.append('backend')

from datacenter import *

warnings.filterwarnings("ignore")


def load_data(ticker, seq_len, normalise_window):
    ds = Stock(ticker)
    data = ds.data

    dataframe_li = []
    for d in data:
        temp = [d['close'], d['open'], d['high'], d['low'], d['volume'], d["vwap"]]
        dataframe_li.append(temp)

    dataframe_li = normalise_data(dataframe_li)

    sequence_length = seq_len + 1
    result = []
    for index in range(len(dataframe_li) - sequence_length):
        result.append(dataframe_li[index: index + sequence_length])

    result = np.array(result)

    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    np.random.shuffle(train)
    x_train = train[:, :-1]
    y_train = train[:, -1][:, -1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1][:, -1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 6))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 6))

    return [x_train, y_train, x_test, y_test]


def get_prediction_data(ticker, seq_len, window):
    ds = Stock(ticker)
    data = ds.data[len(ds.data) - window - 1:]

    dataframe_li = []
    for d in data:
        temp = [d['close'], d['open'], d['high'], d['low'], d['volume'], d["vwap"]]
        dataframe_li.append(temp)

    dataframe_li = normalise_data(dataframe_li)

    sequence_length = seq_len + 1
    result = []
    for index in range(len(dataframe_li) - sequence_length):
        result.append(dataframe_li[index: index + sequence_length])

    result = np.array(result)
    result = result[:, :-1]
    return np.reshape(result, (result.shape[0], result.shape[1], 6))


def normalise_data(li):
    df = pd.DataFrame(li)
    for i in df.columns:
        df[i] = df[i] / df[i].max()
    return df.as_matrix()


def normalise_prices(window_data):
    normalised_data = []
    for i in window_data:
        normalised_window = float(i) / float(window_data[0]) - 1
        normalised_data.append(normalised_window)
    return normalised_data
