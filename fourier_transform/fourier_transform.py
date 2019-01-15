from math import *
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack
sys.path.append('backend')

from datacenter import *
from backend import *


def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


def find_peaks(li, window_size=10):
    if window_size <= 1:
        window_size = 2
    i = 0
    j = i + window_size
    out = []
    mark_type = []
    while j < len(li) - 1:
        subset = li[i:j]
        peak = max(subset)
        trough = min(subset)
        middle_index = int(i + window_size / 2)
        if li[middle_index] == trough:
            if len(mark_type) > 0 and mark_type[-1] == 't':
                if li[middle_index] < li[out[-1]]:
                    out.remove(out[-1])
                    out.append(middle_index)
            else:
                out.append(middle_index)
                mark_type.append('t')

        if li[middle_index] == peak:
            if len(mark_type) > 0 and mark_type[-1] == 'p':
                if li[middle_index] > li[out[-1]]:
                    out.remove(out[-1])
                    out.append(middle_index)
            else:
                out.append(middle_index)
                mark_type.append('p')

        i += 1
        j += 1

    subset = li[out[-1]:len(li) - 1]
    if mark_type[-1] == 'p':
        trough = min(subset)
        out.append(subset.index(trough) + out[-1])
    elif mark_type[-1] == 't':
        peak = max(subset)
        out.append(subset.index(peak) + out[-1])

    return out


stock = Stock(sys.argv[1])
prices = stock.get_data('2015', '2019', 'changePercent')

# Number of samplepoints
N = len(prices)
# sample spacing
T = 1.0 / 100.0

yf = scipy.fftpack.fft(smooth(prices, 20))
xf = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)
yplot = 2.0 / N * np.abs(yf[:N // 2])

fig, ax = plt.subplots()
ax.plot(xf, yplot, '-bo', markevery=find_peaks(yplot.tolist(), 10))
plt.show()
