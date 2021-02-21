import requests
import itertools
import numpy as np
from collections import Counter
from functools import reduce, lru_cache
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 16
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


def parse_rule(rule: str):
    split_str = rule.split(' or ')
    parsed = [[int(n) for n in s.split('-')] for s in split_str]
    return parsed


def check_number(num, rule):
    l1, u1 = rule['rule'][0]
    l2, u2 = rule['rule'][1]
    if (l1 <= num and num <= u1) or (l2 <= num and num <= u2):
        return True
    else:
        return False


def check_ticket(rules, ticket):
    invalid = []
    for t in ticket:
        if not any(check_number(t, r) for r in rules):
            invalid.append(t)
    return invalid
            

def check_tickets(rules, tickets):
    invalids = [check_ticket(rules, t) for t in tickets]
    return invalids


def get_valid_tickets(rules, tickets):
    valids = [t for t in tickets if not check_ticket(rules, t)]
    return valids


def find_field_index(rule, tickets):
    # assumes all tickets are valid
    n_fields = len(tickets[0])
    possible = []
    for i in range(n_fields):
        nums = [t[i] for t in tickets]
        checks = [check_number(n, rule) for n in nums]
        if all(checks):
            possible.append(i)
    return possible


if __name__ == '__main__':
    rules_raw, your_ticket_raw, nearby_tickets_raw = data.split('\n\n')
    rules_list_raw = rules_raw.split('\n')
    rules_list = [r.split(': ') for r in rules_list_raw]
    rules_list = [{'name': r[0], 'rule': parse_rule(r[1])} for r in rules_list]

    your_ticket = your_ticket_raw.split('\n')[1].split(',')

    nearby_tickets = nearby_tickets_raw.split('\n')[1:-1]
    nearby_tickets = [[int(n) for n in nt.split(',')] for nt in nearby_tickets]

    invalid_nums = check_tickets(rules_list, nearby_tickets)
    invalid_sum = sum(sum(i) for i in invalid_nums)
    print('Part 1: ', invalid_sum)

    valid_tickets = get_valid_tickets(rules_list, nearby_tickets)
    possibles = [{'name': rule['name'], 'value': find_field_index(rule, valid_tickets)} for rule in rules_list]
    for i in range(len(rules_list)):
        for p in possibles:
            if len(p['value']) == 1:
                p['index'] = p['value'][0]
                for q in possibles:
                    q['value'] = [v for v in q['value'] if v != p['index']]
    # for p in possibles:
    #     print(p['name'], p['index'])
    deps = [p['index'] for p in possibles if 'departure' in p['name']]
    my_ticket_deps = [int(your_ticket[idx]) for idx in deps]
    answer2 = reduce(lambda x, y: x * y, my_ticket_deps)
    print('Part 2: ', answer2)

