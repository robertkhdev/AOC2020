import requests
import itertools
import numpy as np
from collections import Counter
from functools import reduce, lru_cache
from os import path
from sympy import Matrix, zeros
from diophantine import solve

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 13
data_file = 'day' + str(day) + 'data.txt'
url = 'https://adventofcode.com/2020/day/' + str(day) + '/input'

# save to file and then check if file exists, so I'm not downloading the data every time the script runs.
if path.exists(data_file):
    print('Reading data from file.')
    with open(data_file, 'r') as f:
        data = f.read()
else:
    print('Downloading data.')
    res = requests.get(url, headers={'cookie': cookie})
    data = res.content.decode('utf-8')
    with open(data_file, 'w') as f:
        f.write(data)

start_time, busses = data.rstrip().split('\n')
start_time = int(start_time)
busses_int = [int(b) for b in busses.split(',') if b != 'x']

def first_after_time(bus, time):
    cycles_before = time // bus
    wait_time = (cycles_before + 1) * bus - time
    return wait_time

bus_wait = min([(first_after_time(b, start_time), b) for b in busses_int])

print('Part 1: ', bus_wait[0] * bus_wait[1])

busses = [(int(b), i) for i, b in enumerate(busses.split(',')) if b != 'x']

# busses = [(17, 0), (13, 2), (19, 3)]
# busses = [(67, 0), (7, 1), (59, 2), (61, 3)]
# A = Matrix([[1, 17, 0, 0],
#             [1, 0, 13, 0],
#             [1, 0, 0, 19]])
# b = Matrix([0, 2, 3])
# sol = solve(A, b)[0][0]

A = zeros(len(busses), len(busses) + 1)
for i in range(A.rows):
    A[i, 0] = -1
    A[i, i + 1] = busses[i][0]
b = Matrix([b[1] for b in busses])

sol = solve(A, b)

print('Part 2: ', sol[0][0])

