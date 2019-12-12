import math
import os
import sys
from collections import defaultdict
from typing import List, Tuple, Text, Dict


class Point():
    '''
    Point on the space map
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return self.__repr__().__hash__()

    def distance(self, other):
        '''
        Manhattan distance from this point to another one.
        '''
        return abs(abs(other.x - self.x) + abs(other.y - self.y))

    def view_angle(self, other):
        '''
        Angle of another point relative to this one
        '''
        diff_x = other.x - self.x
        diff_y = other.y - self.y
        if (diff_y == 0):
            return diff_x // abs(diff_x), 0
        if (diff_x == 0):
            return 0, diff_y // abs(diff_y)
        gcd = abs(math.gcd(diff_x, diff_y))
        return diff_x // gcd, diff_y // gcd

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

SpaceMap = List[List[int]]

def get_asteroids_positions(space_map):
    # type: (SpaceMap) -> List[Point]
    '''
    Returns the list of asteroids in the map.
    '''
    asteroids = []
    for y in range(0, len(space_map)):
        for x in range(0, len(space_map[y])):
            if (space_map[y][x] == '#'):
                asteroids.append(Point(x, y))
    return asteroids

def get_asteroid_lines(asteroids):
    # type: (List[Point]) -> List[Tuple[Point, Point]]
    '''
    Return the list of lines from one asteroid to an other one
    '''
    lines = []
    for a in asteroids:
        for b in asteroids:
            if a < b: # Avoids having lines twice with de points inverted
                lines.append((a, b))
    return lines

def get_viewing_angle_and_distance(view_point, asteroids):
    # type: (Point, List[Point]) -> Dict[Tuple[int, int], Dict[int, Point]]
    '''
    Get the viewing angles for all asteroids in the map when viewing from a given position.
    '''
    asteroids_by_angle = defaultdict(dict)
    for asteroid in asteroids:
        if asteroid != view_point:
            asteroids_by_angle[view_point.view_angle(asteroid)][view_point.distance(asteroid)] = asteroid

    return asteroids_by_angle

def is_blocked(line, asteroids):
    # type: (Tuple[Point, Point], List[Point]) -> bool
    '''
    Checks if there is an asteroid blocking the view between two asteroids
    '''
    a, b = line

    for c in asteroids:
        if c < a or c == a:
            continue
        if c == b:
            break
        if a.view_angle(b) == a.view_angle(c):
            return True
    return False


def find_best_spot(space_map):
    # type: (SpaceMap) -> Tuple[Point, int]
    '''
    Finds the asteroid from which the most other asteroids can be viewed
    '''
    viewed = defaultdict(lambda: 0)
    asteroids = get_asteroids_positions(space_map)
    asteroids_lines = get_asteroid_lines(asteroids)

    for line in asteroids_lines:
        if is_blocked(line, asteroids):
            continue
        viewed[line[0]] += 1
        viewed[line[1]] += 1

    best_spot = None
    max_viewed = 0
    for asteroid, nb_viewed in viewed.items():
        if nb_viewed > max_viewed:
            max_viewed = nb_viewed
            best_spot = asteroid

    return best_spot, max_viewed

def convert_angle(x, y):
    # type: (int, int) -> float
    '''
    Converts a viewing angle represented by its x and y coordinates to a degrees angle for the rotating laser
    '''
    if (y == 0):
        if x > 0:
            angle = 90
        else:
            angle = 270
    else:
        angle = 360 * math.atan(x / y) / (2 * math.pi)

    angle = 360 - angle
    if y > 0:
        angle += 180

    return angle % 360

def get_vaporization_list(asteroid, space_map):
    # type: (Point, SpaceMap) -> List[Point]
    '''
    Returns the list of asteroids, in the order they will be vaporized
    '''
    asteroids = get_asteroids_positions(space_map)
    angles_and_distances = get_viewing_angle_and_distance(asteroid, asteroids)

    angles = sorted(angles_and_distances, key=lambda x: convert_angle(x[0], x[1]))

    vaporized = []
    asteroids.remove(asteroid)
    while asteroids:
        initial_length = len(asteroids)
        for angle in angles:
            if len(angles_and_distances[angle]) == 0:
                continue
            distances = sorted(angles_and_distances[angle].keys())
            next_vaporized = angles_and_distances[angle][distances[0]]
            vaporized.append(next_vaporized)
            asteroids.remove(next_vaporized)
            del angles_and_distances[angle][distances[0]]
        if len(asteroids) == initial_length:
            raise Exception('No asteroid vaporized at last rotation !')

    return vaporized

def display_space_map(space_map):
    # type: (SpaceMap) -> None
    '''
    Prints a space map in text mode.
    '''
    for y in range(0, len(space_map)):
        for x in range(0, len(space_map[y])):
            sys.stdout.write(space_map[y][x])
        print('')

def read_space_map(map_file):
    # type: (Text) -> SpaceMap
    '''
    Reads a space map from a file
    '''
    space_map = list()
    with open(os.path.dirname(__file__) + os.sep + map_file + '.txt', 'r') as in_file:
        for line in in_file.readlines():
            space_map.append(list(line.strip()))
    return space_map

def checks_d10p1():
    results = [
        ('test1', Point(5, 8), 33),
        ('test2', Point(1, 2), 35),
        ('test3', Point(6, 3), 41),
        ('test4', Point(11, 13), 210)
    ]

    for map_file, position, count in results:
        space_map = read_space_map(map_file)
        assert find_best_spot(space_map) == (position, count)

def checks_d10p2():
    results = [
        (1, Point(11, 12)),
        (2, Point(12, 1)),
        (3, Point(12, 2)),
        (10, Point(12, 8)),
        (20, Point(16, 0)),
        (50, Point(16, 9)),
        (100, Point(10, 16)),
        (199, Point(9, 6)),
        (200, Point(8, 2)),
        (201, Point(10, 9)),
        (299, Point(11, 1)),
    ]

    space_map = read_space_map('test5')
    vaporized = get_vaporization_list(Point(11, 13), space_map)
    for rank, asteroid in results:
        assert vaporized[rank - 1] == asteroid

def run(with_tests = True):
    if with_tests: checks_d10p1()

    best_spot, d10p1 = find_best_spot(read_space_map('input'))
    print(f'Day 10, Part 1 : {d10p1}') # 263

    if with_tests: checks_d10p2()

    vaporized_200 = get_vaporization_list(best_spot, read_space_map('input'))[199]
    d10p2 = 100 * vaporized_200.x + vaporized_200.y
    print(f'Day 10, Part 2 : {d10p2}') # 1110

if __name__ == '__main__':
    run()
