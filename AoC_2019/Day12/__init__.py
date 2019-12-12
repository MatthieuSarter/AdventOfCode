import  os
import math
from functools import reduce
from typing import List


class Coordinates():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __repr__(self):
        return f'<x={self.x}, y={self.y}, z={self.z}>'

def coordinate_influence(a, b):
    # type: (int, int) -> int
    '''
    Returns -1 if a > b, 0 if a = b, 1 if a < b
    '''
    return (a < b) - (a > b)

class Moon():
    def __init__(self, pos, vel=None):
        self.pos = pos
        self.vel = vel or Coordinates(0,0,0)

    def affect_vel(self, other_moon):
        self.vel.x += coordinate_influence(self.pos.x, other_moon.pos.x)
        self.vel.y += coordinate_influence(self.pos.y, other_moon.pos.y)
        self.vel.z += coordinate_influence(self.pos.z, other_moon.pos.z)

    def apply_vel(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def energy(self):
        return self.pos.energy() * self.vel.energy()

    def __repr__(self):
        return f'pos={self.pos}, vel={self.vel}'

    def __eq__(self, other):
        return self.pos == other.pos

System = List[Moon]

def simulate_step(moons):
    # type: (System) -> None
    '''
    Simulates one system steps
    '''
    for moon in moons:
        [moon.affect_vel(other_moon) for other_moon in moons if not moon is other_moon]
    for moon in moons:
        moon.apply_vel()

def simulate_system(moons, steps):
    # type: (System, int) -> None
    '''
    Simulates several system steps
    '''
    for i in range(0, steps):
        simulate_step(moons)

def total_energy(moons):
    # type: (System) -> int
    '''
    Calculates the energy in the whole system
    '''
    return reduce(int.__add__, map(lambda a: a.energy(), moons))

def axis_energy(axis_configuration):
    return reduce(int.__add__, axis_configuration[0:4]) * reduce(int.__add__, axis_configuration[4:])

def iter_axis(axis_coordinates, axis_speed):
    # type: (List[int], List[int]) -> None
    '''
    Calculates next values for coordinates on a single axis
    '''
    moons_count = len(axis_coordinates)
    for i in range(0, moons_count):
        axis_speed[i] = axis_speed[i] + reduce(int.__add__, [coordinate_influence(axis_coordinates[i], b) for b in axis_coordinates[0:i] + axis_coordinates[i+1:]])
    for i in range(0, moons_count):
        axis_coordinates[i] += axis_speed[i]

def get_axis_period(axis_coordinates, axis_speed):
    # type: (List[int], List[int]) -> int
    '''
    Calculates the period of an axis : the number of steps required to return to the same positions and velocity
    '''
    initial_configuration = (axis_coordinates.copy(), axis_speed.copy())
    period = 0
    while (axis_coordinates, axis_speed) != initial_configuration or period == 0:
        period += 1
        iter_axis(axis_coordinates, axis_speed)

    return period

def get_period(moons):
    # type: (System) -> int
    '''
    Get the period for the whole system

    x, y and z axis are independent, so the period is the lcm of the period of each axis.
    '''
    x_period = get_axis_period([moon.pos.x for moon in moons], [moon.vel.x for moon in moons])
    y_period = get_axis_period([moon.pos.y for moon in moons], [moon.vel.y for moon in moons])
    z_period = get_axis_period([moon.pos.z for moon in moons], [moon.vel.z for moon in moons])

    x_y_period = x_period * y_period // math.gcd(x_period, y_period)
    period = x_y_period * z_period // math.gcd(x_y_period, z_period)

    return period

def checks_d12p1():
    moons = [
        Moon(Coordinates(-1, 0, 2)),
        Moon(Coordinates(2, -10, -7)),
        Moon(Coordinates(4, -8, 8)),
        Moon(Coordinates(3, 5, -1)),
    ]

    simulate_system(moons, 10)
    assert total_energy(moons) == 179

    moons = [
        Moon(Coordinates(-8, -10, 0)),
        Moon(Coordinates(5, 5, 10)),
        Moon(Coordinates(2, -7, 3)),
        Moon(Coordinates(9, -8, -3)),
    ]

    simulate_system(moons, 100)
    assert total_energy(moons) == 1940

def checks_d12p2():
    moons = [
        Moon(Coordinates(-1, 0, 2)),
        Moon(Coordinates(2, -10, -7)),
        Moon(Coordinates(4, -8, 8)),
        Moon(Coordinates(3, 5, -1)),
    ]

    assert get_period(moons) == 2772

    moons = [
        Moon(Coordinates(-8, -10, 0)),
        Moon(Coordinates(5, 5, 10)),
        Moon(Coordinates(2, -7, 3)),
        Moon(Coordinates(9, -8, -3)),
    ]

    assert get_period(moons) == 4686774924


def run(with_tests = True):
    moons = []
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        for line in in_file.readlines():
            moons.append(eval(f'Moon(Coordinates({line.strip()[1:-1]}))'))

    if with_tests: checks_d12p1()

    simulate_system(moons, 1000)
    d12p1 = total_energy(moons)
    print(f'Day 12, Part 1 : {d12p1}') # 7013

    if with_tests: checks_d12p2()
    d12p2 = get_period(moons)
    print(f'Day 12, Part 2 : {d12p2}') # 324618307124784

if __name__ == '__main__':
    run()
