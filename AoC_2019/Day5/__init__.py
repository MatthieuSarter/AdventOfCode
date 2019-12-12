import ast, os
from typing import List, Tuple

from Day2 import checks_d2p1, Program

Input = List[int]
Output = List[int]

def run_program(program, return_output = False, input_list=list()):
    # type: (Program, bool, Input) -> Tuple[Program, Output] or Program
    '''
    Executes an intcode program.
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
    instruction_pointer = 0
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

    if (return_output):
        return program, output
    else :
        return program

def checks_d5p2(intcode_computer):
    progs = [
        [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8],
        [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8],
        [3, 3, 1108, -1, 8, 3, 4, 3, 99],
        [3, 3, 1107, -1, 8, 3, 4, 3, 99],
        [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125,
         20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    ]

    paramss = [
        [7, 8],
        [7, 8],
        [7, 8],
        [7, 8],
        [7, 8, 9]
    ]

    resultss = [
        [0, 1],
        [1, 0],
        [0, 1],
        [1, 0],
        [999, 1000, 1001],
    ]

    for prog, params, results in zip(progs, paramss, resultss):
        for param, result in zip(params, results):
            assert intcode_computer(prog, True, [param])[1].pop() == result

def run(with_tests = True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        program = ast.literal_eval('[' + in_file.read().strip() + ']')

    if with_tests: checks_d2p1(run_program)

    d5p1 = run_program(program, True, [1])[1].pop()
    print(f'Day 5, Part 1 : {d5p1}')  # 9775037

    if with_tests: checks_d5p2(run_program)

    d5p2 = run_program(program, True, [5])[1].pop()
    print(f'Day 5, Part 2 : {d5p2}')  # 15586959


if __name__ == '__main__':
    run()
