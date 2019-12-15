import math
import os
from collections import defaultdict
from typing import Text, Dict, List, Tuple


def parse_chemical_count(value):
    # type: (Text) -> Tuple[Text, int]
    count, chemical = value.strip().split(' ')
    chemical = chemical.strip()
    count = int(count.strip())
    return chemical, count

def get_requirements(chemical, count, reactions):
    if count == 0:
        return {}, 0, 0
    if chemical == 'ORE':
        return {}, 0, count
    reaction_count = reactions[chemical][chemical]
    reaction_iterations = math.ceil(count / reactions[chemical][chemical])

    requirements = {in_chemical: reactions[chemical][in_chemical] * reaction_iterations for in_chemical in reactions[chemical] if in_chemical != chemical and in_chemical != 'ORE'}
    leftover = reaction_count * reaction_iterations - count
    ore = reactions[chemical]['ORE'] * reaction_iterations if 'ORE' in reactions[chemical] else 0
    return requirements, leftover, ore

def get_ore_requirements(chemical, count, reactions, leftovers = None):
    ore = 0
    requirements = defaultdict(lambda: 0, {chemical: count})
    if leftovers is None:
        leftovers = defaultdict(lambda: 0)

    while len(requirements) > 0:
        chemical = next(iter(requirements))
        count = requirements[chemical]
        del requirements[chemical]
        new_requirements, new_leftover, new_ore = get_requirements(chemical, count, reactions)
        ore += new_ore
        leftovers[chemical] += new_leftover
        for new_chemical, new_count in new_requirements.items():
            available = leftovers[new_chemical]
            if available >= new_count:
                leftovers[new_chemical] = available - new_count
            else:
                requirements[new_chemical] += new_count - available
                leftovers[new_chemical] = 0
    return ore, leftovers

def get_fuel_for_ore(ore, reactions):
    fuel = 0
    leftovers = None
    ore_per_fuel = get_ore_requirements('FUEL', 1, reactions, leftovers)[0]
    while ore > 0:
        min_fuel_possible = max(ore // ore_per_fuel, 1)
        consumed_ore, leftovers = get_ore_requirements('FUEL', min_fuel_possible, reactions, leftovers)
        ore -= consumed_ore
        fuel += min_fuel_possible
    return fuel - 1 # stopped with ore < 0, so produced one more FUEL than possible

def checks_d14p1():
    assert get_ore_requirements('FUEL', 1, build_reactions_dict('test1'))[0] == 165
    assert get_ore_requirements('FUEL', 1, build_reactions_dict('test2'))[0] == 13312
    assert get_ore_requirements('FUEL', 1, build_reactions_dict('test3'))[0] == 180697
    assert get_ore_requirements('FUEL', 1, build_reactions_dict('test4'))[0] == 2210736

def checks_d14p2():
    assert get_fuel_for_ore(1000000000000, build_reactions_dict('test2')) == 82892753
    assert get_fuel_for_ore(1000000000000, build_reactions_dict('test3')) == 5586022
    assert get_fuel_for_ore(1000000000000, build_reactions_dict('test4')) == 460664

def build_reactions_dict(file):
    # type: (Text) -> Dict[Text, Dict[Text, int]]
    reactions = dict()
    with open(os.path.dirname(__file__) + os.sep + file + '.txt', 'r') as in_file:
        for reaction in in_file.readlines():
            inputs, output = reaction.strip().split('=>')
            output_chemical, output_count = parse_chemical_count(output)
            reactions[output_chemical] = {output_chemical: output_count}
            for input in inputs.split(','):
                input_chemical, input_count = parse_chemical_count(input)
                reactions[output_chemical][input_chemical] = input_count
    return reactions


def run(with_tests = True):
    checks_d14p1()

    d14p1 = get_ore_requirements('FUEL', 1, build_reactions_dict('input'))[0]
    print(f'Day 14, Part 1 : {d14p1}') # 143173

    checks_d14p2()

    d14p2 = get_fuel_for_ore(1000000000000, build_reactions_dict('input'))
    print(f'Day 14, Part 2 : {d14p2}') # 15988

if __name__ == '__main__':
    run()
