import functools, os, sys

from collections import defaultdict
from typing import List, Tuple, Dict, Text

Circuit = Dict[int, Dict[int, int]]

def build_circuit(instructions):
    # type: (List[str]) -> Circuit
    '''
    Builds the map of a circuit from the instructions list.
    Each cell in the map contains the wire distance from the start point to this cell.
    '''
    circuit = defaultdict(lambda: defaultdict(lambda: 0))
    x = 0
    y = 0
    circuit[x][y] = 1
    steps = 0
    for instruction in instructions:
        direction = instruction[0]
        length = int(instruction[1:])
        if direction == 'R':
            for i in range(1, length + 1):
                x += 1
                steps += 1
                circuit[x][y] = circuit[x][y] or steps
        if direction == 'L':
            for i in range(1, length + 1):
                x -= 1
                steps += 1
                circuit[x][y] = circuit[x][y] or steps
        if direction == 'U':
            for i in range(1, length + 1):
                y += 1
                steps += 1
                circuit[x][y] = circuit[x][y] or steps
        if direction == 'D':
            for i in range(1, length + 1):
                y -= 1
                steps += 1
                circuit[x][y] = circuit[x][y] or steps
    return circuit


def get_circuit_location(circuit):
    # type: (Circuit) -> Tuple[int, int, int, int]
    '''
    Get the max distance from start for all the directions for a given circuit.
    '''
    max_x = max(circuit.keys())
    min_x = min(circuit.keys())
    max_y = 0
    min_y = 0
    for line in circuit.values():
        max_y = max(max(line.keys()), max_y) # type: int
        min_y = min(min(line.keys()), min_y) # type: int
    return min_x, max_x, min_y, max_y


def draw_circuit(circuit):
    # type: (Circuit) -> None
    '''
    Prints a circuit in text mode.
    '''
    min_x, max_x, min_y, max_y = get_circuit_location(circuit)
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            if circuit[x][y]:
                sys.stdout.write('*')
            else:
                sys.stdout.write(' ')
        print('')


def get_circuits_intersections(circuits):
    # type: (List[Circuit]) -> List[Tuple[int, int]]
    '''
    Calculates the list of points where all the given circuits are present.
    '''
    intersections = []
    for x in circuits[0].keys():
        if functools.reduce(lambda x, y: x and y, [x in circuit for circuit in circuits]):
            for y in circuits[0][x].keys():
                if x == 0 and y == 0:  # No intersection at start point
                    continue
                if circuits[0][x][y] == 0:
                    continue

                intersect = functools.reduce(lambda x, y: x and y, [y in circuit[x] for circuit in circuits])
                if intersect:
                    intersections.append((x, y))
    return intersections


def get_closest_intersection_manhattan_distance(circuits_insts):
    # type: (List[List[Text]]) -> Tuple[Tuple[int, int], int]
    '''
    Finds the intersections of all circuits closest to the start point.
    '''
    circuits = [build_circuit(circuit_inst) for circuit_inst in circuits_insts]
    closest = None
    closest_distance = None
    for intersection in get_circuits_intersections(circuits):
        distance = abs(intersection[0]) + abs(intersection[1])
        if not closest_distance or distance < closest_distance:
            closest = intersection
            closest_distance = distance
    return closest, closest_distance


def get_closest_intersection_wire_length(circuits_insts):
    # type: (List[List[Text]]) -> Tuple[Tuple[int, int], int]
    '''
    Finds the intersections of all circuits with the less wire length from the start point.
    '''
    circuits = [build_circuit(circuit_inst) for circuit_inst in circuits_insts]
    closest = None
    closest_distance = None
    for intersection in get_circuits_intersections(circuits):
        distance = functools.reduce(lambda x, y: x + y,
                                    [circuit[intersection[0]][intersection[1]] for circuit in circuits])
        if not closest_distance or distance < closest_distance:
            closest = intersection
            closest_distance = distance
    return closest, closest_distance

tests = [
    ['R8,U5,L5,D3', 'U7,R6,D4,L4', 6, 30],
    ['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83', 159, 610],
    ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 135, 410],
]
def checks_d3p1():
    for circuit1, circuit2, manhattan_distance, _ in tests:
        assert get_closest_intersection_manhattan_distance([circuit1.split(','), circuit2.split(',')])[1] == manhattan_distance

def checks_d3p2():
    for circuit1, circuit2, _, wire_length in tests:
        assert get_closest_intersection_wire_length([circuit1.split(','), circuit2.split(',')])[1] == wire_length


def run():
    circuits_insts_input = []
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        for line in in_file.readlines():
            circuits_insts_input.append(line.strip().split(','))

    checks_d3p1()

    d3p1 = get_closest_intersection_manhattan_distance(circuits_insts_input)[1]
    print(f'Day 3, Part 1 : {d3p1}')  # 248

    checks_d3p2()

    d3p2 = get_closest_intersection_wire_length(circuits_insts_input)[1]
    print(f'Day 3, Part 2 : {d3p2}')  # 28580

if __name__ == '__main__':
    run()