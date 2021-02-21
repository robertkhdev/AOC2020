import requests
import itertools
from collections import Counter
from functools import reduce, lru_cache
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 10
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

data = data.split('\n')
data = [int(d) for d in data if d != '']

data.sort()
device = data[-1] + 3

pairs = zip([0] + data, data + [device])
diffs = Counter([y-x for x, y in pairs])
print('Part 1: ', diffs[1] * diffs[3])

ports = [0] + data + [device]
compatible = {d:[ v for v in ports if d < v and v - d <= 3] for d in ports}

@lru_cache(maxsize=None)
def adapts(jolt):
    if jolt == device:
        return 1
    else:
        return sum(adapts(j) for j in compatible[jolt])


print('Part 2: ', adapts(0))
