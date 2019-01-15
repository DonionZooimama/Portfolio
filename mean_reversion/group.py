import statistics as stats
import sys
import collections
sys.path.append('../backend')

from datacenter import *
from backend import *
from indicators import *

f = open(sys.argv[1])
lines = f.readlines()
symbols = []
for line in lines:
    symbols.append(str(line[:-1]))


for symbol in symbols:
    myDATACENTER = Stock(symbol)
    data = myDATACENTER.data
    volume = []
    for v in data:
        volume.append(int(v['volume']))
    try:
        if stats.mean(volume) > 500000:
            with open("volume.csv", "a") as myfile:
                myfile.write(str(symbol) + '\n')
    except:
        print data
