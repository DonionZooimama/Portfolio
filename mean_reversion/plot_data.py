import matplotlib.pyplot as plt
import statistics as stats
with open("test.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

x = []
y = []
data = []
for line in content:
    split_line = line.split(',')
    if float(split_line[2]) < 0.1 and float(split_line[1]) > 0:
        y.append(float(split_line[3]))

m, d = stats.mean(y), stats.stdev(y)
print m, d

plt.plot(y)

plt.show()
