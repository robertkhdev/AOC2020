import requests
import itertools
from collections import Counter
from functools import reduce
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 9
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

invalid_number = -1
invalid_number_idx = -1

for i in range(len(data) - 25):
    queue = data[i:25 + i]
    if data[25 + i] not in [sum(n) for n in itertools.combinations(queue, 2)]:
        invalid_number_idx = 25 + i
        invalid_number = data[invalid_number_idx]
        break

print('Part 1: ', invalid_number)

weakness = -1
for start in range(invalid_number_idx):
    for end in range(start, invalid_number_idx):
        if sum(data[start:end]) == invalid_number:
            weakness = max(data[start:end]) + min(data[start:end])
            break

print('Part 2: ', weakness)
