import os
from typing import List


def fuel_for_module_1(mass):
    # type:  (int) -> int
    '''
    Compute fuel requirements for a given mass.
    '''
    return max(mass // 3 - 2, 0)

def fuel_for_module_2(mass):
    # type:  (int) -> int
    '''
    Compute fuel requirements for a given mass, including the mass of the fuel itself.
    '''
    total_fuel = 0
    added_fuel = fuel_for_module_1(mass)
    while added_fuel > 0:
        total_fuel += added_fuel
        added_fuel = fuel_for_module_1(added_fuel)
    return total_fuel

def total_fuel(masses, fuel_for_module):
    # type:  (List[int], callable) -> int
    '''
    Compute fuel requirements for a list of modules.
    '''
    total = 0
    for mass in masses:
        total += fuel_for_module(mass)
    return total

def checks_d1p1():
    tests = {
        12: 2,
        14: 2,
        1969: 654,
        100756: 33583
    }

    for mass, fuel in tests.items():
        assert fuel_for_module_1(mass) == fuel

def checks_d1p2():
    tests = {
        12: 2,
        14: 2,
        1969: 966,
        100756: 50346
    }

    for mass, fuel in tests.items():
        assert fuel_for_module_2(mass) == fuel

def run(with_tests = True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        masses = [int(line.strip()) for line in in_file.readlines()]

    if with_tests: checks_d1p1()
    d1p1 = total_fuel(masses, fuel_for_module_1)
    print(f'Day 1, Part 1 : {d1p1}') # 3317970

    if with_tests: checks_d1p2()
    d1p2 = total_fuel(masses, fuel_for_module_2)
    print(f'Day 1, Part 2 : {d1p2}') # 4974073

if __name__ == '__main__':
    run()