import ast, os
from typing import Tuple, List

from Day2 import checks_d2p1, Program
from Day5 import checks_d5p2, Input, Output

Phases = List[int]

def run_program(program, return_output = False, input_list=[], instruction_pointer=0, pause_on_input=False):
    # type: (Program, bool, Input, int, bool) -> Tuple[Program, Output, int] or Tuple[Program, Output] or Program
    '''
    Executes an intcode program.

    There is now a 'pause' feature, returning the current state of execution when waiting for new input, allowing to
    restart the program from where it was left when the new input is available. This avoids handling threads...
    '''
    program = list(program)

    def halt(message):
        print(f'Program: {program}')
        print(f'Pointer: {instruction_pointer}')
        raise Exception(message)

    def get_param_value(instruction, param_number):
        mode = instruction[-param_number - 2:-param_number - 1]
        if mode == '0':
            return program[program[instruction_pointer + param_number]]
        if mode == '1':
            return program[instruction_pointer + param_number]
        halt(f'Unknown parameter mode: {mode}')

    def position_only(instruction, param_number):
        if instruction[-param_number - 2:-param_number - 1] != '0':
            halt(f'Parameter {param_number} must be in position mode')

    def write_result(pointer, value):
        program[program[pointer]] = value

    output = []
    while instruction_pointer < len(program):
        instruction = f'{program[instruction_pointer]:05d}'
        opcode = int(instruction[-2:])
        if opcode in [1, 2, 7, 8]:
            position_only(instruction, 3)
            param1 = get_param_value(instruction, 1)
            param2 = get_param_value(instruction, 2)
            if opcode == 1:
                write_result(instruction_pointer + 3, param1 + param2)
            elif opcode == 2:
                write_result(instruction_pointer + 3, param1 * param2)
            elif opcode == 7:
                write_result(instruction_pointer + 3, 1 if param1 < param2 else 0)
            elif opcode == 8:
                write_result(instruction_pointer + 3, 1 if param1 == param2 else 0)
            instruction_pointer += 4
            continue

        if opcode in [5, 6]:
            param = get_param_value(instruction, 1)
            if (opcode == 5 and param != 0) or (opcode == 6 and param == 0):
                instruction_pointer = get_param_value(instruction, 2)
            else:
                instruction_pointer += 3
            continue

        if opcode == 3:
            position_only(instruction, 1)
            value = None
            while not isinstance(value, int):
                try:
                    if not input_list and pause_on_input:
                        return program, output, instruction_pointer
                    value = input_list.pop(0) if input_list else int(input('Enter int value: '))
                except ValueError:
                    pass
            write_result(instruction_pointer + 1, value)
            instruction_pointer += 2
            continue

        if opcode == 4:
            output.append(get_param_value(instruction, 1))
            instruction_pointer += 2
            continue

        if opcode == 99:
            break
        halt(f'Unknown opcode: {opcode}')

    if pause_on_input:
        return program, output, -1
    if return_output:
        return program, output
    return program


def run_amp_chain(program, phases):
    # type: (Program, Phases) -> int
    '''
    Computes the output signal of a amp chain.
    '''
    value = 0
    for phase in phases:
        value = run_program(program, True, [phase, value])[1].pop()
    return value


def generate_phases(nb_amp, phase_values):
    # type: (int, Phases) -> List[Phases]
    '''
    Computes all the allowed phases combinations.
    '''
    if nb_amp == 0:
        return [[]]
    res = []
    phase_values = set(phase_values)
    if (len(phase_values) < nb_amp):
        raise Exception('There must be at least one phase value per amp')
    for phase in phase_values:
        remaining_phases = set(phase_values)
        remaining_phases.remove(phase)
        for phases in generate_phases(nb_amp - 1, list(remaining_phases)):
            res.append([phase] + phases)
    return res


def find_best_phases(program, nb_amp=5, phase_values=[0, 1, 2, 3, 4]):
    # type: (Program, int, Phases) -> Tuple[Phases, int]
    '''
    Finds the phases combination giving the higher output.
    '''
    best_phases = None
    best_result = 0
    for phases in generate_phases(nb_amp, phase_values):
        result = run_amp_chain(program, phases)
        if result > best_result:
            best_phases = phases
            best_result = result
    return best_phases, best_result


def run_amp_chain_loop(program, phases):
    # type: (Program, Phases) -> int
    '''
    Computes the output signal of a amp chain with retroaction loop.
    '''
    value = 0
    programs = [program for i in range(0, len(phases))]
    pointers = [0 for i in range(0, len(phases))]
    first_loop = True
    while True:
        for i in range(0, len(phases)):
            if pointers[i] == -1:
                return value
            if first_loop:
                params = [phases[i], value]
            else:
                params = [value]
            res = run_program(programs[i], True, params, pointers[i], True)
            programs[i], output, pointers[i] = res
            if output:
                value = output.pop()
        first_loop = False


def find_best_phases_loop(program, nb_amp=5, phase_values=[5, 6, 7, 8, 9]):
    # type: (Program, int, Phases) -> Tuple[Phases, int]
    '''
    Finds the phases combination giving the higher output for an amp chain with retroaction.
    '''
    best_phases = None
    best_result = 0
    for phases in generate_phases(nb_amp, phase_values):
        result = run_amp_chain_loop(program, phases)
        if result > best_result:
            best_phases = phases
            best_result = result
    return best_phases, best_result

def checks_d7p1():
    progs = [
        [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
        [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0],
        [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31,
         31, 4, 31, 99, 0, 0, 0]
    ]
    best_phases = [
        [4, 3, 2, 1, 0],
        [0, 1, 2, 3, 4],
        [1, 0, 4, 3, 2]
    ]
    results = [
        43210,
        54321,
        65210
    ]
    for prog, phases, results in zip(progs, best_phases, results):
        assert run_amp_chain(prog, phases) == results
        assert find_best_phases(prog)[0] == phases

def checks_d7p2():
    progs = [
        [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0,
         5],
        [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1,
         53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0,
         0, 10]
    ]
    best_phases = [
        [9, 8, 7, 6, 5],
        [9, 7, 8, 5, 6]
    ]
    results = [
        139629729,
        18216
    ]
    for prog, phases, results in zip(progs, best_phases, results):
        assert run_amp_chain_loop(prog, phases) == results
        assert find_best_phases_loop(prog)[0] == phases

def run(with_tests = True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        program = ast.literal_eval('[' + in_file.read().strip() + ']')

    if with_tests:
        checks_d2p1(run_program)
        checks_d5p2(run_program)

        checks_d7p1()

    d7p1 = find_best_phases(program)[1]
    print(f'Day 7, Part 1 : {d7p1}')  # 225056

    if with_tests: checks_d7p2()

    d7p2 = find_best_phases_loop(program)[1]
    print(f'Day 7, Part 2 : {d7p2}')  # 14260332


if __name__ == '__main__':
    run()
