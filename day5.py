import requests
import itertools
import functools
from collections import Counter
from functools import reduce
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 5
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
data = [d.replace('\n', '') for d in data]

def get_half(half, rng):
    lo, hi = rng
    if int(hi) == int(lo + 1):
        if half == 'F' or half == 'L':
            return lo
        else:
            return hi
    if half == 'F'  or half == 'L':
        return lo, (hi - lo + 1) / 2 - 1 + lo
    else:
        return (hi - lo + 1) / 2 + lo, hi

# get_half('F', get_half('B', get_half('F', (0, 127))))
# assert get_half('F', (0, 127)) == (0, 63)
# assert get_half('B', (0, 63)) == (32, 63)
# assert get_half('F', (32, 63)) == (32, 47)
# assert get_half('B', (32, 47)) == (40, 47)
# assert get_half('B', (40, 47)) == (44, 47)
# assert get_half('F', (44, 47)) == (44, 45)

# functools.reduce(lambda x,y: get_half(y,x), 'FBFBBFF', (0, 127))

def parse_seat(s) -> int:
    fb = s[:7]
    lr = s[7:]
    row = functools.reduce(lambda x,y: get_half(y,x), fb, (0, 127))
    col = functools.reduce(lambda x,y: get_half(y,x), lr, (0, 7))
    return row * 8 + col

# parse_seat('FBFBBFFRLR')
# parse_seat('BFFFBBFRRR')
# parse_seat('FFFBBBFRRR')
# parse_seat('BBFFBBFRLL')

hi_id = max(parse_seat(d) for d in data)
print('Part 1: ', hi_id)


max_seat = 127 * 8 + 7
seats = set(parse_seat(d) for d in data)
for i in range(max_seat):
    if i not in seats and i-1 in seats and i+1 in seats:
        print(i)

