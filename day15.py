import requests
import itertools
import numpy as np
from collections import Counter
from functools import reduce, lru_cache
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 15
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

data = data.split(',')
data = [int(d) for d in data]


def gap(game_list):
    # reverse list and then drop first element
    num = game_list[-1]
    rev = list(reversed(game_list))[1:]
    if num not in rev:
        return 0
    else:
        gap = rev.index(num) + 1
        return gap

# data = [0, 3, 6]
# data = [1, 3, 2]


# def play_game(turns, data):
#     starting_nums = data[:]
#     starting_nums.reverse()
#     numbers = []
#     for i in range(turns):
#         if len(starting_nums) > 0:
#             # append in reverse order to match original order
#             numbers.append(starting_nums.pop())
#         else:
#             numbers.append(gap(numbers))
#         if i % 100000 == 0:
#             print(i)
#     return numbers[-1]


print('Part 1: ', play_game(2020, data))

def play_game(turns, data):
    # key is number spoken and value is last turn it was spoken
    game = dict()
    starting_nums = list(reversed(data))
    last_num = 0
       # NEED TO TRACK LAST TWO TIMES NUMBER IS SAID *************************
    for i in range(turns):
        if len(starting_nums) > 0:
            # append in reverse order to match original order
            last_num = starting_nums.pop()
            game[last_num] = [i, i]
        else:
            if game[last_num][0] == game[last_num][1]:
                last_num = 0
                if last_num not in game.keys():
                    game[last_num] = [i, i]
                else:
                    game[0] = [game[0][1], i]
            else:
                # not first occurence
                last_num = game[last_num][1] - game[last_num][0]
                if last_num not in game.keys():
                    game[last_num] = [i, i]
                else:
                    game[last_num] = [game[last_num][1], i]

        # print(last_num)
        if i % 100000 == 0:
            print(i)
    return last_num

runs = 30000000
# play_game(runs, [0,3,6])
# play_game(runs, [1,3,2])
# play_game(runs, [2,1,3])
# play_game(runs, [1,2,3])
# play_game(runs, [2,3,1])
# play_game(runs, [3,2,1])
# play_game(runs, [3,1,2])

print('Part 2: ', play_game(30000000, data))
