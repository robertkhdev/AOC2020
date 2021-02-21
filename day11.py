import requests
import itertools
from collections import Counter
from functools import reduce, lru_cache
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 11
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

# data = data.split('\n')
data = [list(d.replace('\n', '')) for d in data]

def count_adjacent(i, j, grid):
    cols = len(grid[0]) - 1
    rows = len(grid) - 1
    count = 0
    if i > 0 and j > 0:
        if grid[i-1][j-1] == '#': count += 1
    if i > 0:
        if grid[i-1][j] == '#': count += 1
    if i > 0 and j < cols:
        if grid[i-1][j+1] == '#': count += 1
    if j > 0:
        if grid[i][j-1] == '#': count += 1
    if i < rows and j > 0:
        if grid[i+1][j-1] == '#': count += 1
    if i < rows:
        if grid[i+1][j] == '#': count += 1
    if i < rows and j < cols:
        if grid[i+1][j+1] == '#': count += 1
    if j < cols:
        if grid[i][j+1] == '#': count += 1
    return count


def new_state(i, j, grid):
    if grid[i][j] == 'L' and count_adjacent(i, j, grid) == 0:
        return '#'
    elif grid[i][j] == '#' and count_adjacent(i, j, grid) >= 4:
        return 'L'
    else:
        return grid[i][j]


def step(orig):
    rows = len(orig)
    cols = len(orig[0])
    return [[new_state(i, j, orig) for j in range(cols)] for i in range(rows)]


def print_grid(grid, rows=10, cols=5):
    [print(''.join(row[:rows])) for row in grid[:cols]]


def grid_diff(g1, g2):
    g1 = [item for sublist in g1 for item in sublist]
    g2 = [item for sublist in g2 for item in sublist]
    pairs = zip(g1, g2)
    diffs = [p for p in pairs if p[0] != p[1]]
    return len(diffs)


test_grid = ['L.LL.LL.LL',
            'LLLLLLL.LL',
            'L.L.L..L..',
            'LLLL.LL.LL',
            'L.LL.LL.LL',
            'L.LLLLL.LL',
            '..L.L.....',
            'LLLLLLLLLL',
            'L.LLLLLL.L',
            'L.LLLLL.LL']


def count_occupied(grid):
    return len([item for sublist in grid for item in sublist if item == '#'])

g1 = data[:]
# g1 = test_grid[:]
while True:
    # print_grid(g1, None, None)
    g2 = step(g1)
    # occupied1 = count_occupied(g1)
    # occupied2 = count_occupied(g2)
    # print(grid_diff(g1, g2), occupied1, occupied2)
    if grid_diff(g1, g2) == 0:
        break
    g1 = g2[:]

occupied = len([item for sublist in g2 for item in sublist if item == '#'])
print('Part 1: ', occupied)

def first_seat_in_dir(i, j, i_dir, j_dir, grid):
    """
    i_dir and j_dir must be one of [-1, 0, 1]
    """
    max_i = len(grid) - 1
    max_j = len(grid[0]) - 1
    i_next = i + i_dir
    j_next = j + j_dir
    if i_next < 0 or i_next > max_i: return ''
    if j_next < 0 or j_next > max_j: return ''
    while grid[i_next][j_next] == '.':
        i_next += i_dir
        j_next += j_dir
        if i_next < 0 or i_next > max_i: return ''
        if j_next < 0 or j_next > max_j: return ''
    return grid[i_next][j_next]

def count_first_adjacent(i, j, grid):
    inds = list(itertools.product([0,1,-1],repeat=2))
    inds.remove((0, 0))
    return len([ind for ind in inds if first_seat_in_dir(i, j, ind[0], ind[1], grid) == '#'])

def new_state2(i, j, grid):
    if grid[i][j] == 'L' and count_first_adjacent(i, j, grid) == 0:
        return '#'
    elif grid[i][j] == '#' and count_first_adjacent(i, j, grid) >= 5:
        return 'L'
    else:
        return grid[i][j]

def step2(orig):
    rows = len(orig)
    cols = len(orig[0])
    return [[new_state2(i, j, orig) for j in range(cols)] for i in range(rows)]

g1 = data[:]
# g1 = test_grid[:]
while True:
    # print_grid(g1, None, None)
    g2 = step2(g1)
    # occupied1 = count_occupied(g1)
    # occupied2 = count_occupied(g2)
    # print(grid_diff(g1, g2), occupied1, occupied2)
    if grid_diff(g1, g2) == 0:
        break
    g1 = g2[:]

occupied = len([item for sublist in g2 for item in sublist if item == '#'])
print('Part 2: ', occupied)
