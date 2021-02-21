import requests
import itertools
from collections import Counter
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

data_file = 'day2data.txt'
url = 'https://adventofcode.com/2020/day/2/input'

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


def count_letter(letter, word):
    counts = Counter(word)
    if letter in counts:
        return counts[letter]
    return 0


def is_valid_password(row):
    rule, letter, password = row
    letter_count = count_letter(letter, password)
    if letter_count < rule[0] or letter_count > rule[1]:
        return False
    return True


def is_valid_password2(row):
    rule, letter, password = row
    pos1 = password[rule[0]-1] == letter
    pos2 = password[rule[1]-1] == letter
    if pos1 + pos2 != 1:
        return False
    return True


def process_row(row, validation_func):
    r = row.split(' ')
    ret = []
    ret.append(tuple([int(d) for d in r[0].split('-')]))
    ret.append(r[1].replace(':', ''))
    ret.append(r[2].replace('\n', ''))
    return validation_func(ret)


result = [process_row(d, is_valid_password) for d in data]
print('Part 1: ', sum(result))

result2 = [process_row(d, is_valid_password2) for d in data]
print('Part 2: ', sum(result2))

