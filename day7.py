import requests
import itertools
from collections import Counter
from functools import reduce
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 7
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


raw_data = data[:]


def parse_row(row: str):
    row = row.replace(' bags', '')
    row = row.replace(' bag', '')
    row = row.replace('.\n', '')
    row = row.split(' contain ')
    key, value = row
    value = ''.join([v for v in value if v not in '0123456789'])
    values = value.split(', ')
    values = [v.lstrip() for v in values]
    return key, values

# test = ['light red bags contain 1 bright white bag, 2 muted yellow bags.\n',
#         'dark orange bags contain 3 bright white bags, 4 muted yellow bags.\n',
#         'bright white bags contain 1 shiny gold bag.\n',
#         'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.\n',
#         'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.\n',
#         'dark olive bags contain 3 faded blue bags, 4 dotted black bags.\n',
#         'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.\n',
#         'faded blue bags contain no other bags.\n',
#         'dotted black bags contain no other bags.\n']

# test = dict(parse_row(r) for r in test)
# can_hold = set()
# for d in test:
#     if d not in can_hold:
#         if contains(test[d], test, can_hold):
#             can_hold.add(d)


data = dict(parse_row(r) for r in data)
can_hold = set()

def contains(bags, data, can_hold):
    # if isinstance(bags, str): 
    #     bags = [bags]
    if 'shiny gold' in bags:
        return True
    if 'no other' in bags:
        return False
    if any(b in can_hold for b in bags):
        return True
    else:
        return any(contains(data[b], data, can_hold) for b in bags)


for d in data:
    if d not in can_hold:
        if contains(data[d], data, can_hold):
            can_hold.add(d)


print('Part 1: ', len(can_hold))


def extract_num(v):
    if 'no other' in v:
        return (1, 'no other')
    else:
        return (int(v[0]), v[2:])


def parse_row2(row: str):
    row = row.replace(' bags', '')
    row = row.replace(' bag', '')
    row = row.replace('.\n', '')
    row = row.split(' contain ')
    key, value = row
    # value = ''.join([v for v in value if v not in '0123456789'])
    values = value.split(', ')
    values = [v.lstrip() for v in values]
    values = [extract_num(v) for v in values]
    return key, values


def count_up(bags, data):
    # if isinstance(bags, str): 
    #     bags = [bags]
    # if 'shiny gold' in bags:
    #     return True
    # print(data[bags[0][1]])
    if 'no other' == bags[0][1]:
        return 0
    else:
        n = sum(count_up(data[b[1]], data) * b[0] + b[0] for b in bags) - sum(1 for b in bags if b[1] == 'no other')
        return n


data2 = raw_data


# test = ['shiny gold bags contain 2 dark red bags.\n',
#         'dark red bags contain 2 dark orange bags.\n',
#         'dark orange bags contain 2 dark yellow bags.\n',
#         'dark yellow bags contain 2 dark green bags.\n',
#         'dark green bags contain 2 dark blue bags.\n',
#         'dark blue bags contain 2 dark violet bags.\n',
#         'dark violet bags contain no other bags.\n']

# test = dict(parse_row2(r) for r in test)
# test['no other'] = (1, '')
# count_up(test['shiny gold'], test)

data2 = dict(parse_row2(r) for r in data2)
data2['no other'] = (1, '')
print('Part 2: ', count_up(data2['shiny gold'], data2))
