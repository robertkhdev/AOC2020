import requests
import itertools
from collections import Counter
from functools import reduce
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 6
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

data = ''.join(data)
data = data.split('\n\n')
data1 = [d.replace('\n', '') for d in data]
# data = [d.split(' ') for d in data]
print('Part 1: ', sum([len(set(d)) for d in data1]))

data2 = [d.rstrip().split('\n') for d in data]
intersects = [set.intersection(*[set(a) for a in d]) for d in data2]
print('Part 2: ', sum([len(i) for i in intersects]))