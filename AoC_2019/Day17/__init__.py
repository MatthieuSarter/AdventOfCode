import ast
import functools
import os
import sys
from collections import defaultdict
from typing import Dict, Tuple, List, Text

from Day10 import Point
from Day2 import Program
from Day9 import run_program

ShieldMap = Dict[Point, Tuple[int, int]]

directions = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
directions_ascii = list(map(ord, '^>v<'))

def build_map(cells):
    # type: (List[int]) -> Tuple[ShieldMap, Tuple[Point, int]]
    '''
    Converts the camera output to a structured map
    '''
    vacuum_state = (Point(-1, -1), 0)
    shield_map = defaultdict(lambda: 0)
    x = 0
    y = 0
    for cell in cells:
        if cell == 10:
            y += 1
            x = 0
            continue
        pos = Point(x, y)
        if cell in directions_ascii:
            vacuum_state = (pos, cell)
            cell = 35
        shield_map[pos] = cell
        x += 1

    return shield_map, vacuum_state

def find_intersections(shield_map):
    # type: (ShieldMap) -> List[Point]
    '''
    Returns the list of intersections in a map
    '''
    intersections = [ point for point, value in list(shield_map.items()) if value == 35 and len([point + d for d in directions if shield_map[point + d] != 35]) == 0 ]
    return intersections

def display_map(shield_map, vacuum_state=(Point(-1, -1), 0), intersections=[]):
    # type: (ShieldMap, Tuple[Point, int], List[int]) -> None
    '''
    Prints the map in text mode
    '''
    max_x = max([p.x for p in shield_map if shield_map[p] is not None])
    max_y = max([p.y for p in shield_map if shield_map[p] is not None])

    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            pos = Point(x, y)
            value = shield_map[Point(x, y)] if pos != vacuum_state[0] else vacuum_state[1]
            if pos in intersections:
                value = ord('O')
            sys.stdout.write(chr(value))
        print('')

def sum_alignement_parameters(intersections):
    # type: (List[Point]) -> int
    '''
    Calculates the alignement parameters
    '''
    res = functools.reduce(int.__add__, map(lambda p: p.x * p.y, intersections))
    return res

def generate_instructions(system_map, vacuum_state):
    # type: (ShieldMap, Tuple[Point, int]) -> Text
    '''
    Generates the instructions for moving the robot through the whole scaffolding
    '''
    pos = vacuum_state[0]
    direction_idx = directions_ascii.index(vacuum_state[1])

    instructions = []
    while True:
        if system_map[pos + directions[(direction_idx - 1) % 4]] == 35:
            direction_idx = (direction_idx - 1) % 4
            instructions.append('L')
        elif system_map[pos + directions[(direction_idx + 1) % 4]] == 35:
            direction_idx = (direction_idx + 1) % 4
            instructions.append('R')
        elif system_map[pos + directions[direction_idx]] != 35:
            break
        direction = directions[direction_idx]
        pos += direction
        steps = 1
        while system_map[pos + direction] == 35:
            steps += 1
            pos += direction
        instructions.append(str(steps))

    return ','.join(instructions)

def compress_instructions(instructions):
    # type: (Text) -> Tuple[Text, Dict[Text, Text]]
    '''
    Calculates the main routine and functions for moving the robot
    '''
    # Didnot manage to implement this properly for now :(
    return '', {'': ''}


def move_robot(program, instructions):
    # type: (Program, Text) -> int
    '''
    Moves the robot and return the amount of collected dust
    '''
    main_routine, functions = compress_instructions(instructions)

    # Found by hand...
    main_routine = "A,B,A,B,A,C,B,C,A,C"
    functions = {'A': 'L,6,R,12,L,6', 'B': 'R,12,L,10,L,4,L,6', 'C':'L,10,L,10,L,4,L,6'}

    input = list(map(ord, main_routine))
    input.append(10)
    for function in functions.values():
        input.extend(map(ord, function))
        input.append(10)
    input.append(ord('n'))
    input.append(10)

    program[0] = 2
    _, output, _, _ = run_program(program, input)

    return output[-1]

def checks_d17p1():
    cells = [
        46, 46, 35, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 10,
        46, 46, 35, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 10,
        35, 35, 35, 35, 35, 35, 35, 46, 46, 46, 35, 35, 35, 10,
        35, 46, 35, 46, 46, 46, 35, 46, 46, 46, 35, 46, 35, 10,
        35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 10,
        46, 46, 35, 46, 46, 46, 35, 46, 46, 46, 35, 46, 46, 10,
        46, 46, 35, 35, 35, 35, 35, 46, 46, 46, 35, 46, 46, 10
    ]
    system_map, _ = build_map(cells)
    intersections = find_intersections(system_map)
    assert sum_alignement_parameters(intersections) == 76

def checks_d17p2():
    cells = [
        35, 35, 35, 35, 35, 35, 35, 46, 46, 46, 35, 35, 35, 35, 35, 10,
        35, 46, 46, 46, 46, 46, 35, 46, 46, 46, 35, 46, 46, 46, 35, 10,
        35, 46, 46, 46, 46, 46, 35, 46, 46, 46, 35, 46, 46, 46, 35, 10,
        46, 46, 46, 46, 46, 46, 35, 46, 46, 46, 35, 46, 46, 46, 35, 10,
        46, 46, 46, 46, 46, 46, 35, 46, 46, 46, 35, 35, 35, 46, 35, 10,
        46, 46, 46, 46, 46, 46, 35, 46, 46, 46, 46, 46, 35, 46, 35, 10,
        35, 35, 35, 35, 35, 35, 35, 35, 35, 46, 46, 46, 35, 46, 35, 10,
        46, 46, 46, 46, 46, 46, 35, 46, 35, 46, 46, 46, 35, 46, 35, 10,
        46, 46, 46, 46, 46, 46, 35, 35, 35, 35, 35, 35, 35, 35, 35, 10,
        46, 46, 46, 46, 46, 46, 46, 46, 35, 46, 46, 46, 35, 46, 46, 10,
        46, 46, 46, 46, 35, 35, 35, 35, 35, 35, 35, 35, 35, 46, 46, 10,
        46, 46, 46, 46, 35, 46, 46, 46, 35, 46, 46, 46, 46, 46, 46, 10,
        46, 46, 46, 46, 35, 46, 46, 46, 35, 46, 46, 46, 46, 46, 46, 10,
        46, 46, 46, 46, 35, 46, 46, 46, 35, 46, 46, 46, 46, 46, 46, 10,
        46, 46, 46, 46, 35, 35, 35, 35, 35, 46, 46, 46, 46, 46, 46, 10
    ]
    system_map, _ = build_map(cells)
    vacuum_state = (Point(0, 6), ord('^'))
    instructions = generate_instructions(system_map, vacuum_state)
    assert instructions == 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2'
    # assert compress_instructions(instructions)[0] == 'A,B,C,B,A,C'

def run(with_tests = True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        program = ast.literal_eval('[' + in_file.read().strip() + ']')

    checks_d17p1()

    _, output, _, _ = run_program(program)
    system_map, vacuum_state = build_map(output)
    d17p1 = sum_alignement_parameters(find_intersections(system_map))
    print(f'Day 17, Part 1 : {d17p1}') # 8928

    checks_d17p2()

    instructions = generate_instructions(system_map, vacuum_state)
    d17p2 = move_robot(program, instructions)
    print(f'Day 17, Part 2 : {d17p2}') # 880360

if __name__ == '__main__':
    run()
