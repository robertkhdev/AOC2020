import requests
import itertools
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

data_file = 'day1data.txt'
url = 'https://adventofcode.com/2020/day/1/input'

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

data = [int(d) for d in data if d != '']

combos = itertools.combinations(data, 2)
valid_combos = [c for c in combos if sum(c) == 2020]
result = valid_combos[0][0] * valid_combos[0][1]
result

combos3 = itertools.combinations(data, 3)
valid_combos3 = [c for c in combos3 if sum(c) == 2020]
result3 = valid_combos3[0][0] * valid_combos3[0][1] * valid_combos3[0][2]
result3