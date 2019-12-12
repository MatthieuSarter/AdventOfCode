import ast, os
import sys
from collections import defaultdict, namedtuple
from typing import Tuple, Dict

from Day9 import run_program, NewProgram, convert_program

from Day10 import Point

PaintedArea = Dict[int, Dict[int, int]]
Direction = namedtuple('Direction', ('x', 'y'))

def paint(program, start_color):
    # type: (NewProgram, int) -> Tuple[int, PaintedArea]
    '''
    Run a painting program on the robot
    '''
    directions = [Direction(0, -1), Direction(1, 0), Direction(0, 1), Direction(-1, 0)]
    painted_area = defaultdict(lambda: defaultdict(lambda: -1))
    painted_area[0][0] = start_color
    position = Point(0, 0)
    direction = 0
    pointer = 0
    relative_base = 0
    while pointer != -1:
        current_color = max(painted_area[position.y][position.x], 0)
        program, output, pointer, relative_base = run_program(program, [current_color], pointer, True, relative_base)
        painted_area[position.y][position.x] = output[0]
        if output[1] == 1:
            direction = (direction + 1) % len(directions)
        else:
            direction = (direction - 1) % len(directions)

        position.x = position.x + directions[direction].x
        position.y = position.y + directions[direction].y

    nb_painted = 0
    for y in painted_area:
        for x in painted_area[y]:
            if painted_area[y][x] > -1:
                nb_painted += 1

    return nb_painted, painted_area

def display_paint(painted_area):
    # type: (PaintedArea) -> None
    '''
    Prints a painted area in text mode.
    '''
    min_x, max_x = 0, 0
    for y in painted_area:
        min_x = min(min(painted_area[y]), min_x)
        max_x = max(max(painted_area[y]), max_x)

    for y in sorted(painted_area):
        for x in range(min_x, max_x + 1):
            if (painted_area[y][x]) == 1:
                sys.stdout.write('█')
            else:
                sys.stdout.write(' ')
        print('')

def run(with_tests = True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        program = ast.literal_eval('[' + in_file.read().strip() + ']')

    d11p1, p= paint(convert_program(program), 0)
    print(f'Day 11, Part 1 : {d11p1}') # 2056

    _, d11p2 = paint(convert_program(program), 1)
    print('Day 11, Part 2 :') # GLBEPJZP
    display_paint(d11p2)



if __name__ == '__main__':
    run()
