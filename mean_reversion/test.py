import numpy as np
import statistics as stats
import pandas as pd
import sys
import collections
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


f = open(sys.argv[1])
lines = f.readlines()
symbols = []
for line in lines:
    symbols.append(str(line[:-1]))


for symbol in symbols:
    myDATACENTER = Stock(symbol)
    data = myDATACENTER.data

    dataframe_li = []
    for d in data:
        try:
            temp = [d['open'], d['high'], d['low'], d['close'], d['volume']]
        except KeyError:
            continue
        dataframe_li.append(temp)

    df = pd.DataFrame(dataframe_li, columns=['open', 'high', 'low', 'close', 'volume'])

    try:
        s, e = mean_reversion_score(df, 5)
        daily_return = []
        for i in range(len(e.equity) - 1):
            daily_return.append(percent_change(e.equity[i], e.equity[i + 1]))

        sharpe_ratio = stats.mean(daily_return) / stats.stdev(daily_return)
        sharpe_ratio = sharpe_ratio * (252 ** 0.5)
        with open("test.txt", "a") as myfile:
            myfile.write(str(symbol) + ',' + str(s) + ',' + str(stats.mean(e.trade_roi)) + ',' + str(max_drawdown(e.equity)) + ',' + str(e.get_winrate()) + ',' + str(sharpe_ratio) + ',' + str(e.winners + e.lossers) + ',' + str(stats.mean(df['volume'])) + '\n')
    except:
        print 'idk but', symbol, 'is dumb'
