import ast, os
import sys
from collections import defaultdict
from typing import Dict, Tuple

from Day10 import Point
from Day9 import run_program, Program

SectionMap = Dict[Point, int]

directions = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]
next_direction = [2, 3, 1, 0] # next_direction[i] is the direction to take if the droid hit the wall when moving in
                              # direction i. This keeps the wall to the right.

def print_map(section_map, droid_position):
    # type: (SectionMap, Point) -> None
    '''
    Prints the map in text mode.
    '''
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

    xs = [p.x for p in section_map]
    min_x, max_x = min(xs), max(xs)
    ys = [p.y for p in section_map]
    min_y, max_y = min(ys), max(ys)

    symbols = {-2: '░', -1: '█', 1: ' ', 2: '●', 3: '¤', 4: '☺'}
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Point(x, y) == droid_position:
                sys.stdout.write(symbols[4])
            else:
                value = section_map[Point(x, y)]
                sys.stdout.write(symbols[value])
        print('')

def build_map(program):
    # type: (Program) -> Tuple[SectionMap, SectionMap, Point]
    '''
    Builds the section map by keeping the wall to the right
    '''
    section_map = defaultdict(lambda: -2, {Point(0, 0): 3})
    distance_map = defaultdict(lambda: sys.maxsize, {Point(0,0): 0})

    pointer = 0
    relative_base = 0
    direction = 1
    position = Point(0, 0)
    oxygen_system_location = None

    while pointer != -1:
        program, output, pointer, relative_base = run_program(program, [direction + 1], pointer, True, relative_base)
        result = output[0]
        if result == 0:
            section_map[position + directions[direction]] = -1
            # Droid hit a wall, change the direction to keep the wall on the right
            direction = next_direction[direction]
        else:
            position += directions[direction]
            section_map[position] = max(section_map[position], result)
            distance_map[position] = min([distance_map[position + directions[i]] for i in range(0, 4)]) + 1
            if result == 2:
                oxygen_system_location = position
            # Droid didn't hit a wall, go back to the previous direction to keep the wall on the right
            direction = next_direction.index(direction)
        # Back to the start and all direction from the start are known, the map is completed
        if position == Point(0, 0) and section_map[directions[0]] != -2 and section_map[directions[1]] != -2 and section_map[directions[2]] != -2 and section_map[directions[3]] != -2:
            break
    return section_map, distance_map, oxygen_system_location

def get_fill_time(system_map, oxygen_location):
    # type: (SectionMap, Point) -> int
    '''
    Calculates the time to fill the whole section.
    '''
    time = -1 # need to start at -1, as time to fill oxygen_location will be counted
    filled = []
    new_filled = [oxygen_location]
    while new_filled:
        filled.extend(new_filled)
        time += 1
        next_filled = []
        for point in new_filled:
            next_filled.extend([p for p in [point + directions[i] for i in range(0, 4)] if p not in filled and system_map[p] >= 0])
        new_filled = next_filled
    return time


def run(with_tests = True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        program = ast.literal_eval('[' + in_file.read().strip() + ']')

    section_map, distance_map, oxygen_system_location = build_map(program)
    d15p1 = distance_map[oxygen_system_location]
    print(f'Day 15, Part 1 : {d15p1}') # 262

    d15p2 = get_fill_time(section_map, oxygen_system_location)
    print(f'Day 15, Part 2 : {d15p2}') # 15988

if __name__ == '__main__':
    run()
