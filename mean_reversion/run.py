import numpy as np
import statistics as stats
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ohlc
import pandas as pd
import sys
sys.path.append('../backend')

from datacenter import *
from backend import *
from indicators import *


def rolling_mean_reversion_score(df, n, window):
    rolling_avg_price, upper_band, lower_band = Bolinger_Bands(df['open'], n, 1)
    out = np.zeros_like(df['open'])
    for i in range(n + window, len(df['open'])):
        exchange = stock_exchange(100000)
        bought_in = False
        for j in range(i - window, i):
            if bought_in is False:
                if df['open'][j] < lower_band['open'][j]:
                    exchange.buy(exchange.capital, df['open'][j])
                    bought_in = True
                elif df['low'][j] < lower_band['open'][j]:
                    exchange.buy(exchange.capital, lower_band['open'][j])
                    bought_in = True
            else:
                if df['open'][j] > rolling_avg_price['open'][j]:
                    bought_in = False
                    exchange.sell(exchange.shares, df['open'][j])
                elif df['high'][j] > upper_band['open'][j]:
                    bought_in = False
                    exchange.sell(exchange.shares, upper_band['open'][j])
                elif df['high'][j] > rolling_avg_price['open'][j]:
                    bought_in = False
                    exchange.sell(exchange.shares, rolling_avg_price['open'][j])

            exchange.update_equity(df['close'][j])

        out[i] = (exchange.equity[-1] - 100000) / 100000

    return out


def mean_reversion_score(df, n):
    rolling_avg_price, upper_band, lower_band = Bolinger_Bands(df['open'], n, 1)
    bought_in = False
    exchange = stock_exchange(10000)

    for i in range(df.iloc[0].name, df.iloc[-1].name):
        if bought_in is False:
            if df['open'][i] < lower_band['open'][i]:
                exchange.buy(exchange.capital, df['open'][i])
                bought_in = True
            elif df['low'][i] < lower_band['open'][i]:
                exchange.buy(exchange.capital, lower_band['open'][i])
                bought_in = True
        else:
            if df['high'][i] > upper_band['open'][i]:
                bought_in = False
                exchange.sell(exchange.shares, upper_band['open'][i])

        exchange.update_equity(df['close'][i])

    if len(exchange.equity) == 0:
        return [0, 0]
    out = (exchange.equity[-1] - 10000) / 10000
    pc = []
    for i in range(1, len(exchange.equity)):
        pc.append((exchange.equity[i] - exchange.equity[i - 1]) / exchange.equity[i - 1])

    return out, exchange


def rolling_hurst(df, window):
    out = np.zeros_like(df['open'])
    for i in range(window + 1, len(df['open'])):
        out[i] = hurst(df['close'][i - window: i].tolist())

    return out


myDATACENTER = Stock(sys.argv[1])
data = myDATACENTER.data

dataframe_li = []
for d in data:
    try:
        temp = [d['open'], d['high'], d['low'], d['close']]
    except KeyError:
        continue
    dataframe_li.append(temp)

df = pd.DataFrame(dataframe_li, columns=['open', 'high', 'low', 'close'])

s, e = mean_reversion_score(df, 5)

print s
print max_drawdown(e.equity)

exchange2 = stock_exchange(10000)

exchange2.buy(exchange2.capital, df['open'][0])
exchange2.sell(exchange2.shares, df['close'][len(df['close']) - 1])


plt.plot(e.equity)

plt.show()
