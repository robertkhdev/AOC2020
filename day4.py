import requests
import itertools
from collections import Counter
from functools import reduce
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 4
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
data = [d.replace('\n', ' ') for d in data]
data = [d.split(' ') for d in data]

def create_dict(row):
    items = [r.split(':') for r in row if ':' in r]
    return dict(items)
    

def is_valid(d, req_fields):
    return all(r in d.keys() for r in req_fields)

dicts = [create_dict(r) for r in data]

req_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

num_valid = sum(1 for d in dicts if is_valid(d, req_fields))
print('Part 1: ', num_valid)


def is_valid2(d, req_fields) -> bool:
    if not is_valid(d, req_fields): return False
    if int(d['byr']) < 1920 or int(d['byr']) > 2002: return False
    if int(d['iyr']) < 2010 or int(d['iyr']) > 2020: return False
    if int(d['eyr']) < 2020 or int(d['eyr']) > 2030: return False
    hgt_num = int(d['hgt'][:-2])
    if d['hgt'][-2:] == 'cm':
        if hgt_num < 150 or hgt_num > 193: return False
    elif d['hgt'][-2:] == 'in':
        if hgt_num < 59 or hgt_num > 76: return False
    else:
        return False
    if d['hcl'][0] != '#' or len(d['hcl']) != 7: return False
    if not all(n in '0123456789abcdef' for n in d['hcl'][1:]): return False
    if not d['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}: return False
    if len(d['pid']) != 9 or not all(n in '0123456789' for n in d['pid']): return False
    # if 'cid' in d: del d['cid']
    # print(sorted(d.items()))
    return True


valid = [d for d in dicts if is_valid2(d, req_fields)]
num_valid2 = len(valid)
print('Part 2: ', num_valid2)