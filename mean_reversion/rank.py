import operator
import pandas as pd

f = open('test.txt')
lines = f.readlines()
data = []


def bubble(li, index):
    for i in range(len(li) - 1):
        for j in range(i, len(li) - 1):
            if float(li[j][index]) > float(li[j + 1][index]):
                temp = li[j]
                li[j] = li[j + 1]
                li[j + 1] = temp

    return li


def find_index(li, symbol):
    index = 0
    for i in li:
        if symbol.lower() == i[0].lower():
            return index
        index += 1
    return -1


for line in lines:
    line_data = str(line[:-1]).split(',')
    if int(line_data[5]) > 200 and int(line_data[7]) > 100000:
        for i in range(1, len(line_data)):
            line_data[i] = float(line_data[i])
        data.append(line_data)

df = pd.DataFrame(data, columns=['name', 'precent_change', 'precent_change_per_trade', 'max_drawdown', 'winrate', 'trades', 'volume'])

df['precent_change'] = (df['precent_change'] - df['precent_change'].mean()) / df['precent_change'].std()
df['precent_change_per_trade'] = (df['precent_change_per_trade'] - df['precent_change_per_trade'].mean()) / df['precent_change_per_trade'].std()
df['max_drawdown'] = (df['max_drawdown'] - df['max_drawdown'].mean()) / df['max_drawdown'].std()
df['winrate'] = (df['winrate'] - df['winrate'].mean()) / df['winrate'].std()
df['trades'] = (df['trades'] - df['trades'].mean()) / df['trades'].std()
df['volume'] = (df['volume'] - df['volume'].mean()) / df['volume'].std()

print df.head()
exit(-1)


scores = []

for d in data:
    scores.append([d[0], 0])

indicies = [2, 3, 4]
for i in indicies:
    data = bubble(data, i)
    if i == 3:
        data.reverse()
    rank = 0
    for d in data:
        current_index = find_index(scores, d[0])
        scores[current_index][1] += rank
        rank += 1

scores = bubble(scores, 1)
for s in scores:
    print s
