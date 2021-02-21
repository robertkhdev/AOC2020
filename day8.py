import requests
import itertools
from collections import Counter
from functools import reduce
from os import path

with open('./AOCcookie.txt', 'r') as f:
    cookie = f.read()

day = 8
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
data = [d.split(' ') for d in data]
data = [(d[0], int(d[1])) for d in data]

class Computer():
    def __init__(self, program):
        self.program = program
        self.ptr = 0
        self.accumulator = 0
    
    def run(self):
        visited = set()
        repeat = False
        done = False
        exit_type = ''
        while not repeat and not done:
            if self.ptr in visited:
                repeat = True
                exit_type = 'Breaking Loop'
                break
            if self.ptr > len(self.program) - 1:
                done = True
                exit_type = 'Normal Exit'
                break
            visited.add(self.ptr)
            inst = self.program[self.ptr]
            # print(self.ptr, inst)
            opcode = inst[0]
            arg = inst[1]
            if opcode == 'nop':
                self.ptr += 1
            elif opcode == 'acc':
                self.accumulator += arg
                self.ptr += 1
            elif opcode == 'jmp':
                self.ptr += arg
        return exit_type, self.accumulator

print('Part 1: ', Computer(data).run())

data[412] = ('nop', 161)

for i in range(len(data)):
    data_try = data[:]
    if data_try[i][0] == 'nop':
        data_try[i] = ('jmp', data_try[i][1])
    elif data_try[i][0] == 'jmp':
        data_try[i] = ('nop', data_try[i][1])
    result = Computer(data_try).run()
    if result[0] == 'Normal Exit':
        print('Part 2: ', result[1])
