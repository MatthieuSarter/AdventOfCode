import ast
import os
import sys

from Day10 import Point
from Day9 import run_program

def get_status(x, y, program):
    _, output, _, _ = run_program(program, [x, y])
    return output[0] == 1

def get_affected_points(program, width=50, height=50):
    affected_points = set()
    for y in range(0, height):
        for x in range(0, width):
            if get_status(x, y, program):
                affected_points.add(Point(x, y))
    return affected_points

def display_beam(affected_points, start_x=0, start_y=0):
    height = max(p.y for p in affected_points)
    width = max(p.x for p in affected_points)
    for y in range(start_y, height):
        for x in range(start_x, width):
            sys.stdout.write('#' if Point(x, y) in affected_points else '.')
        print('')

def find_closest_n_square(program, n=100):
    beam_starts = {n-1: 0}
    y = n
    while True:
        x = beam_starts[y-1]
        beam_starts[y] = x
        while x < 2 * y: # there are some lines without beam at the begining so we limit the number of position to test even if beam is not found
            if get_status(x, y, program):
                beam_starts[y] = x
                # Are other corners of the square in the beam ?
                if y > n and get_status(x + n - 1, y, program) and get_status(x, y - n + 1, program) and get_status(x + n - 1, y - n + 1, program):
                    return Point(x, y - n + 1)
                break
            x += 1
        y += 1


def run(with_tests = True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        program = ast.literal_eval('[' + in_file.read().strip() + ']')

    d19p1 = len(get_affected_points(program))
    print(f'Day 19, Part 1 : {d19p1}') # 226

    #display_beam(get_affected_points(program, 30,30), 18, 22)

    pos = find_closest_n_square(program, 100)
    d19p2 = pos.x * 10000 + pos.y
    print(f'Day 19, Part 2 : {d19p2}') # 7900946

if __name__ == '__main__':
    run()
