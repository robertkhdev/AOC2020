import requests
import itertools
import numpy as np
from collections import Counter
from functools import reduce, lru_cache
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 12
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

data = data.split('\n')
data = [(d[0], int(d[1:])) for d in data if d != '']

# represent state as tuple (direction, (NS_coord, EW_coord))
# direction in an integer that maps to the cardinal directions
# N = 0
# E = 1
# S = 2
# W = 3
# initial state = (1, (0, 0))

def convert_dir_str(dir_chr):
    return {'N': 0, 'E': 1, 'S': 2, 'W': 3}[dir_chr]

def convert_dir_num(dir_num):
    return {0: 'N', 1: 'E', 2: 'S', 3: 'W'}[dir_num]

def step(state, move):
    action, value = move
    s_dir, s_coords = state
    new_state = ()
    if action == 'N':
        new_state = (s_dir, (s_coords[0] + value, s_coords[1]))
    if action == 'S':
        new_state = (s_dir, (s_coords[0] - value, s_coords[1]))
    if action == 'E':
        new_state = (s_dir, (s_coords[0], s_coords[1] + value))
    if action == 'W':
        new_state = (s_dir, (s_coords[0], s_coords[1] - value))
    if action == 'L':
        turns = value  // 90
        s_dir = convert_dir_str(s_dir)
        new_dir = (s_dir - turns ) % 4
        new_dir = convert_dir_num(new_dir)
        new_state = (new_dir, s_coords)
    if action == 'R':
        turns = value  // 90
        s_dir = convert_dir_str(s_dir)
        new_dir = (s_dir + turns ) % 4
        new_dir = convert_dir_num(new_dir)
        new_state = (new_dir, s_coords)
    if action == 'F':
        if s_dir == 'N':
            new_state = (s_dir, (s_coords[0] + value, s_coords[1]))
        if s_dir == 'E':
            new_state = (s_dir, (s_coords[0], s_coords[1] + value))
        if s_dir == 'S':
            new_state = (s_dir, (s_coords[0] - value, s_coords[1]))
        if s_dir == 'W':
            new_state = (s_dir, (s_coords[0], s_coords[1] - value))
    return new_state


state = ('E', (0, 0))
# state = step(state, ('F', 10))
# state = step(state, ('N', 3))
# state = step(state, ('F', 7))
# state = step(state, ('R', 90))
# state = step(state, ('F', 11))
# state

end = reduce(step, data, state)
print('Part 1: ', abs(end[1][0]) + abs(end[1][1]))

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def step_wp(state, move):
    action, value = move
    wp, loc = state
    new_wp = ()
    if action == 'N':
        new_wp = (wp[0] + value, wp[1])
    if action == 'S':
        new_wp = (wp[0] - value, wp[1])
    if action == 'E':
        new_wp = (wp[0], wp[1] + value)
    if action == 'W':
        new_wp = (wp[0], wp[1] - value)
    if action == 'L':
        rho, phi = cart2pol(wp[1], wp[0])
        phi += value / 180 * np.pi
        x, y = pol2cart(rho, phi)
        new_wp = (round(y), round(x))
    if action == 'R':
        rho, phi = cart2pol(wp[1], wp[0])
        phi -= value / 180 * np.pi
        x, y = pol2cart(rho, phi)
        new_wp = (round(y), round(x))
    if action == 'F':
        loc = (loc[0] + value * wp[0], loc[1] + value * wp[1])
        new_wp = wp
    return new_wp, loc

state = ((1, 10), (0, 0))
end = reduce(step_wp, data, state)
print('Part 2: ', abs(end[1][0]) + abs(end[1][1]))
