import ast, os
from collections import defaultdict
from typing import Tuple, Dict

from Day2 import Program, checks_d2p1
from Day5 import Input, Output, checks_d5p2

NewProgram = Dict[int, int]

def run_program(program, input_list=[], instruction_pointer=0, pause_on_input=False, relative_base = 0):
    # type: (NewProgram or Program, Input, int, bool, int) -> Tuple[NewProgram, Output, int, int]
    '''
    Executes an intcode program.
    '''
    if type(program) == list:
        program = convert_program(program)
    else:
        program = program.copy()

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
        if mode == '2':
            return program[relative_base + program[instruction_pointer + param_number]]
        halt(f'Unknown parameter mode: {mode}')

    def position_only(instruction, param_number):
        if instruction[-param_number - 2:-param_number - 1] not in ['0', '2']:
            halt(f'Parameter {param_number} must be in position or relative mode')

    def write_result(instruction, param_number, value):
        mode = instruction[-param_number -2:-param_number - 1]
        if mode == '0':
            program[program[instruction_pointer + param_number]] = value
        if mode == '2':
            program[relative_base + program[instruction_pointer + param_number]] = value

    output = []
    while instruction_pointer < len(program):
        instruction = f'{program[instruction_pointer]:05d}'
        opcode = int(instruction[-2:])
        if opcode in [1, 2, 7, 8]:
            position_only(instruction, 3)
            param1 = get_param_value(instruction, 1)
            param2 = get_param_value(instruction, 2)
            if opcode == 1:
                write_result(instruction, 3, param1 + param2)
            elif opcode == 2:
                write_result(instruction, 3, param1 * param2)
            elif opcode == 7:
                write_result(instruction, 3, 1 if param1 < param2 else 0)
            elif opcode == 8:
                write_result(instruction, 3, 1 if param1 == param2 else 0)
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
                        return program, output, instruction_pointer, relative_base
                    value = input_list.pop(0) if input_list else int(input('Enter int value: '))
                except ValueError:
                    pass
            write_result(instruction, 1, value)
            instruction_pointer += 2
            continue

        if opcode == 4:
            output.append(get_param_value(instruction, 1))
            instruction_pointer += 2
            continue

        if opcode == 9:
            relative_base += get_param_value(instruction, 1)
            instruction_pointer += 2
            continue

        if opcode == 99:
            break
        halt(f'Unknown opcode: {opcode}')

    return program, output, -1, relative_base

def convert_program(program):
    # type: (Program) -> NewProgram
    '''
    Convert old programs (list) to new programs (dict).
    '''
    return defaultdict(lambda: 0, enumerate(program))

def run_program_compat(program, return_output = False, input_list=[], instruction_pointer=0, pause_on_input=False):
    # type: (Program, bool, Input, int, bool) -> Tuple[Program, Output, int] or Tuple[Program, Output] or Program
    '''
    Executes old programs on the new computer.
    '''
    program, output, pointer, _ = run_program(convert_program(program), input_list, instruction_pointer, pause_on_input, 0)

    program = list(program.values())

    if pause_on_input:
        return program, output, -1
    if return_output:
        return program, output
    return program

def checks_d9p1():
    program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    _, output, _, _ = run_program(convert_program(program))
    assert output == program

    program = [1102,34915192,34915192,7,4,7,99,0]
    _, output, _, _ = run_program(convert_program(program))
    assert len(str(output.pop())) == 16

    program = [104,1125899906842624,99]
    _, output, _, _ = run_program(convert_program(program))
    assert output.pop() == 1125899906842624

def run(with_tests: True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        program = ast.literal_eval('[' + in_file.read().strip() + ']')

    if with_tests:
        checks_d2p1(run_program_compat)
        checks_d5p2(run_program_compat)

        checks_d9p1()

    d9p1 = run_program(convert_program(program), [1])[1].pop()
    print(f'Day 9, Part 1 : {d9p1}') # 3533056970

    d9p2 = run_program(convert_program(program), [2])[1].pop()
    print(f'Day 9, Part 2 : {d9p2}') # 72852

if __name__ == '__main__':
    run()
