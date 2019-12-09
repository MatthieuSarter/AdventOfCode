import functools, os
from typing import Text, Dict, List

SpaceMap = Dict[Text, Text]
Path = List[Text]

def count_orbits_for_element(data, element, calculated_orbits):
    # type: (SpaceMap, Text, Dict[Text, int]) -> int
    '''
    Count the number of orbited elements for a given element.
    '''
    if element in calculated_orbits:
        return calculated_orbits[element]
    if element == 'COM':
        orbits = 0
    else:
        orbits = 1 + count_orbits_for_element(data, data[element], calculated_orbits)
    calculated_orbits[element] = orbits
    return orbits


def count_orbits(data):
    # type: (SpaceMap) -> int
    '''
    Count the number of orbits in the space.
    '''
    orbits_by_element = dict()
    for element in data.keys():
        count_orbits_for_element(data, element, orbits_by_element)
    return functools.reduce(lambda x, y: x + y, orbits_by_element.values())


def path_to_com(data, element):
    # type: (SpaceMap, Text) -> Path
    '''
    Compute the path from an element to the COM.
    '''
    if element == 'COM':
        return []
    return [data[element]] + path_to_com(data, data[element])


def path_to_target(data, element, target):
    # type: (SpaceMap, Text, Text) -> Path
    '''
    Compute the path from an element to an other.
    '''
    element_to_com = path_to_com(data, element)
    com_to_target = path_to_com(data, target)[::-1]
    for step in element_to_com:
        if step in com_to_target:
            break
    return element_to_com[0:element_to_com.index(step)] + com_to_target[com_to_target.index(step):]

def checks_d6p1():
    test_data = {
        'B': 'COM', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E', 'G': 'B', 'H': 'G', 'I': 'D', 'J': 'E', 'K': 'J', 'L': 'K'
    }
    assert count_orbits(test_data) == 42

def checks_d6p2():
    test_data = {
        'B': 'COM', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E', 'G': 'B', 'H': 'G', 'I': 'D', 'J': 'E', 'K': 'J', 'L': 'K', 'YOU': 'K', 'SAN': 'I'
    }
    assert path_to_target(test_data, 'YOU', 'SAN') == ['K', 'J', 'E', 'D', 'I']


def run():
    data = {}
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        for line in in_file.readlines():
            parent, child = line.strip().split(')')
            data[child] = parent

    checks_d6p1()

    d6p1 = count_orbits(data)
    print(f'Day 6, Part 1 : {d6p1}')  # 119831

    checks_d6p1()

    d6p2 = len(path_to_target(data, 'YOU', 'SAN')) - 1;
    print(f'Day 6, Part 2 : {d6p2}')  # 322

if __name__ == '__main__':
    run()
