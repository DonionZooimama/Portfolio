import datacenter as dc
import numpy as np
import statistics as stats
import pandas as pd
from numpy import *
import sys


def rsi(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100.0 - 100.0 / (1.0 + rs)
    for i in range(n, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.0
        else:
            upval = 0.0
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n
        rs = up / down
        rsi[i] = 100.0 - 100.0 / (1.0 + rs)

    return list(rsi)


def Bolinger_Bands(stock_price, window_size, num_of_std):
    df = pd.DataFrame(stock_price)
    rolling_mean = df.rolling(window=window_size).mean()
    rolling_std = df.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)

    return rolling_mean, upper_band, lower_band


def find_turningpoints(opens, closes=5, window=5):
    out = []
    if isinstance(closes, int):
        window = closes
        closes = opens

    for i in range(window, len(opens) - 1):
        open_subset = opens[i - window: i]
        close_subset = closes[i - window: i]

        upper_subset = []
        lower_subset = []
        subset = []
        mid = window // 2

        for j in range(len(close_subset)):
            if open_subset[j] > close_subset[j]:
                upper_subset.append(open_subset[j])
                lower_subset.append(close_subset[j])
            else:
                upper_subset.append(close_subset[j])
                lower_subset.append(open_subset[j])
            subset.append(open_subset[j])
            subset.append(close_subset[j])

        if upper_subset[mid] == max(subset):
            out.append([i - mid - 1, upper_subset[mid]])
        elif lower_subset[mid] == min(subset):
            out.append([i - mid - 1, lower_subset[mid]])

    return out


def moving_average(li, n=3):
    out = np.zeros_like(li)

    for j in range(n, len(li)):
        subset = li[j - n: j]
        out[j] = stats.mean(subset)

    return out.tolist()


def percent_change(x1, x2):
    return ((x2 - x1) / x2)


def is_doji(open, close, thresh_hold=0.25):
    change = percent_change(open, close)
    if abs(change) < thresh_hold:
        return True
    else:
        return False


def min_max_normalization(li):

    out = []
    min_value = min(li)
    max_value = max(li)
    for x in li:
        out.append((x - min_value) / (max_value - min_value))
    return out


def hurst(p):
    tau = []
    lagvec = []
    #  Step through the different lags
    for lag in range(2, 20):
        #  produce price difference with lag
        pp = subtract(p[lag:], p[:-lag])
        #  Write the different lags into a vector
        lagvec.append(lag)
        #  Calculate the variance of the differnce vector
        tau.append(sqrt(std(pp)))
    #  linear fit to double-log graph (gives power)
    m = polyfit(log10(lagvec), log10(tau), 1)
    # calculate hurst
    hurst = m[0] * 2
    return hurst


def max_drawdown(li):
    mdd = 0
    for i in range(len(li)):
        dd = 0
        for j in range(i + 1, len(li)):
            dd = percent_change(li[i], li[j])
            if dd >= 0:
                break
            if dd < mdd:
                mdd = dd

    return mdd
