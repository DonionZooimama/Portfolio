import sys

f = open(sys.argv[1])
lines = f.readlines()
data = []
for line in lines:
    line = line[:-1]
    data.append(line.split(','))

summation = 0
total = 0
for d in data:
    summation += float(d[2])
    total += int(d[-1])

print summation / len(data)
print total

summation = 0
for d in data:
    summation += float(d[1])
