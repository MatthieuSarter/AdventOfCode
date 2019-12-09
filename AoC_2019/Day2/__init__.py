import ast, os
from typing import List

Program = List[int]

def run_program(program):
    # type: (Program) -> Program
    '''
    Executes an intcode program.
    '''
    pointer = 0
    while pointer < len(program):
        if program[pointer] == 1:
            program[program[pointer + 3]] = program[program[pointer + 1]] + program[program[pointer + 2]]
            pointer += 4
            continue
        if program[pointer] == 2:
            program[program[pointer + 3]] = program[program[pointer + 1]] * program[program[pointer + 2]]
            pointer += 4
            continue
        if program[pointer] == 99:
            return program
        raise Exception("Something went wrong")
    return program

def find_noun_verb_for_result(program, result):
    # type: (Program, int) -> int
    '''
    Finds the combination of input required to generate a given output with a given program.
    '''
    for noun in range(0, 100):
        for verb in range(0, 100):
            program[1] = noun
            program[2] = verb
            try:
                if run_program(list(program))[0] == result:
                    return 100 * noun + verb
            except:
                pass
    raise Exception('No parameters for this result')

def checks_d2p1(intcode_computer):
    progs = [
        [1, 0, 0, 0, 99],
        [2, 3, 0, 3, 99],
        [2, 4, 4, 5, 99, 0],
        [1, 1, 1, 4, 99, 5, 6, 0, 99]
    ]

    results = [
        [2, 0, 0, 0, 99],
        [2, 3, 0, 6, 99],
        [2, 4, 4, 5, 99, 9801],
        [30, 1, 1, 4, 2, 5, 6, 0, 99]
    ]

    for prog, result in zip(progs, results):
        assert intcode_computer(prog) == result

def run():
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        program = ast.literal_eval('[' + in_file.read().strip() + ']')

    checks_d2p1(run_program)

    program[1] = 12
    program[2] = 2
    d2p1 = run_program(list(program))[0]
    print(f'Day 2, Part 1 : {d2p1}')  # 9581917

    d2p2 = find_noun_verb_for_result(program, 19690720)
    print(f'Day 2, Part 2 : {d2p2}')  # 2505

if __name__ == '__main__':
    run()