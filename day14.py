import requests
import itertools
import numpy as np
from collections import Counter
from functools import reduce, lru_cache
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 14
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

data = data.split('\n')[:-1]

def parse_item(d):
    d = d.split(' = ')
    item = dict()
    if d[0] == 'mask':
        item['command'] = 'mask'
        item['mask'] = d[1]
    elif d[0][:3] == 'mem':
        item['command'] = 'mem'
        loc = int(d[0].replace('mem[', '').replace(']', ''))
        item['loc'] = loc
        item['val'] = int(d[1])
    return item

def bit_mask(mask, bit):
    if mask == 'X':
        return bit
    else:
        return mask


def apply_mask(num ,mask):
    b_num = '{0:036b}'.format(num)
    comb = zip(mask, b_num)
    masked_int = int(''.join([bit_mask(c[0], c[1]) for c in  comb]), 2)
    return masked_int



mem = dict()
mask = '{0:036b}'.format(0)
for d in data:
    command = parse_item(d)
    if command['command'] == 'mask':
        mask = command['mask']
    if command['command'] == 'mem':
        num = command['val']
        mem[command['loc']] = apply_mask(num, mask)

print('Part 1: ', sum(mem.values()))



def bit_mask2(mask, bit):
    if mask == 'X':
        return 'X'
    elif mask == '1':
        return '1'
    else:
        return bit


def apply_mask2(num ,mask):
    b_num = '{0:036b}'.format(num)
    comb = zip(mask, b_num)
    masked_str = ''.join([bit_mask2(c[0], c[1]) for c in  comb])
    return masked_str


def replace_x(bits, replacements):
    bits = list(bits)
    for i, b in enumerate(bits):
        if b == 'X':
            bits[i] = replacements.pop()
    return ''.join(bits)


def get_mems(masked_addr):
    count = Counter(masked_addr)
    if 'X' in count.keys():
        c = count['X']
        prod = list(itertools.product('01', repeat=c))
        return [replace_x(masked_addr, list(p)) for p in prod]
    else:
        return [masked_addr]


mem = dict()
mask = '{0:036b}'.format(0)
for d in data:
    command = parse_item(d)
    if command['command'] == 'mask':
        mask = command['mask']
    if command['command'] == 'mem':
        num = command['val']
        loc = command['loc']
        masked = apply_mask2(loc, mask)
        mems_to_write = get_mems(masked)
        for m in mems_to_write:
            mem[int(m, 2)] = num


print('Part 2: ', sum(mem.values()))