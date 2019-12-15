import ast, os
import sys
from collections import defaultdict
from time import sleep
from typing import Dict, List

from Day10 import Point
from Day9 import run_program, NewProgram, convert_program

GameMap = Dict[Point, int]

def count_tiles(program, tile_type):
    # type: (NewProgram, int) -> int
    '''
    Count the number of tiles of a given type.
    '''
    _, output, _, _ = run_program(program)
    count = 0
    for i in range(0, len(output) // 3):
        if output[3 * i + 2] == tile_type:
            count += 1

    return count

def update_game_map(output, game_map=None):
    # type: (List[int], GameMap) -> GameMap
    '''
    Updates the game map with the program's output
    '''
    if game_map is None:
        game_map = defaultdict(lambda: 0)
    for i in range(0, len(output) // 3):
        x = output[3 * i]
        y = output[3 * i + 1]
        value = output[3 * i + 2]
        game_map[Point(x, y)] = value

    return game_map

def print_game_map(game_map):
    # type: (GameMap) -> None
    '''
    Print the game map in text mode
    '''
    os.system('clear')
    symbols = [' ', '█', '░', '▬', '●']
    max_x = max([p.x for p in game_map])
    max_y = max([p.y for p in game_map])
    print(f'Score: {game_map[Point(-1, 0)]}')
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            value = game_map[Point(x, y)]
            sys.stdout.write(symbols[value])
        print('')

def find_object(game_map, object):
    # type: (GameMap, int) -> Point
    '''
    Finds the position of the first occurence a given object in the game map
    '''
    for p, value in game_map.items():
        if value == object:
            return p

def play(program, fps=0):
    # type: (NewProgram, int) -> int
    '''
    Play the game until it ends
    '''
    program[0] = 2
    pointer = 0
    relative_base = 0
    input = []
    game_map = None
    while pointer != -1:
        program, output, pointer, relative_base = run_program(program, input, pointer, True, relative_base)
        game_map = update_game_map(output, game_map)
        if fps:
            print_game_map(game_map)
            sleep(1 / fps)
        paddle_pos = find_object(game_map, 3)
        ball_pos = find_object(game_map, 4)
        if (ball_pos is None or paddle_pos is None):
            input = [0]
            continue
        input = [(ball_pos.x > paddle_pos.x) - (ball_pos.x < paddle_pos.x)]
    if fps:
        print_game_map(update_game_map(output, game_map))
    return game_map[Point(-1, 0)]

def run(with_tests = True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        program = ast.literal_eval('[' + in_file.read().strip() + ']')

    d13p1 = count_tiles(program, 2)
    print(f'Day 13, Part 1 : {d13p1}') # 326

    d13p2 = play(program)
    print(f'Day 13, Part 2 : {d13p2}') # 15988

if __name__ == '__main__':
    run()
