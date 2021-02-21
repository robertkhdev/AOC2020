import requests
import itertools
from collections import Counter
from functools import reduce
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 3
data_file = 'day' + str(day) + 'data.txt'
url = 'https://adventofcode.com/2020/day/' + str(day) + '/input'

# save to file and then check if file exists, so I'm not downloading the data every time the script runs.
if path.exists(data_file):
    print('Reading data from file.')
    with open(data_file, 'r') as f:
        data = f.readlines()
else:
    print('Downloading data.')
    res = requests.get(url, headers={'cookie': cookie})
    data = res.content.decode('utf-8')
    with open(data_file, 'w') as f:
        f.writelines(data)

data = [d.replace('\n', '') for d in data]


def count_trees(data, slope, display=False):
    x, y = slope
    trees = 0
    cols = len(data[0])
    n = 0
    for i in range(1, len(data)):
        hit = False
        if i % y == 0:
            n = (n + x) % cols
            if data[i][n] == '#':
                trees += 1
                hit = True
        if display:
            icon = 'X' if hit else 'O'
            orig = data[i]
            new = list(orig)
            if i % y == 0:
                new[n] = icon
            print(i, orig, ''.join(new))
    return trees

print(count_trees(data, (3, 1)))

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
trees = [count_trees(data, s) for s in slopes]
print(reduce(lambda x,y: x*y, trees))

# count_trees(data[:], (1,2), True)