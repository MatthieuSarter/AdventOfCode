import functools
import os
from typing import List, Text


def checks_d16p1():
    assert apply_fft_with_fast_fft("12345678", 1) == "48226158"
    assert apply_fft_with_fast_fft("12345678", 2) == "34040438"
    assert apply_fft_with_fast_fft("12345678", 3) == "03415518"
    assert apply_fft_with_fast_fft("80871224585914546619083218645595", 100)[0:8] == "24176176"
    assert apply_fft_with_fast_fft("19617804207202209144916044189917", 100)[0:8] == "73745418"
    assert apply_fft_with_fast_fft("69317163492948606335995924319873", 100)[0:8] == "52432133"

def checks_d16p2():
    pass

def get_fft_pattern(position, length):
    # type: (int, int) -> List[int]
    '''
    Get the pattern for calculating the nth digit of the output.
    '''
    base_pattern = [0, 1, 0, -1]
    pattern = []
    for i in range(0, position * len(base_pattern)):
        pattern.append(base_pattern[i // position])

    repeats = length // len(pattern) + 1
    pattern = pattern * repeats

    return pattern[1:length + 1]

def apply_fft(sequence, iterations):
    # type: (Text, int) -> Text
    '''
    Apply the FFT n time on a message.
    '''
    sequence = list(map(int, sequence))
    length = len(sequence)
    patterns = [get_fft_pattern(i + 1, length) for i in range(0, length)]
    for iter in range(0, iterations):
        sequence = [abs(functools.reduce(int.__add__, [s * p for s, p in zip(sequence, patterns[i])])) % 10 for i in range(0, length)]
    return ''.join(map(str, sequence))

def apply_fft_with_fast_fft(sequence, iterations = 1):
    # type: (Text, int) -> Text
    '''
    Apply the FFT n time on a message.
    '''
    sequence = list(map(int, sequence))
    length = len(sequence)
    patterns = [get_fft_pattern(i + 1, length) for i in range(0, length // 2)]
    for iter in range(0, iterations):
        first_half = [abs(functools.reduce(int.__add__, [s * p for s, p in zip(sequence, patterns[i])])) % 10 for i in range(0, length // 2)]
        second_half = apply_fast_fft(sequence[length // 2:])
        sequence = first_half + second_half
    return ''.join(map(str, sequence))

def apply_fast_fft(sequence, iterations = 1):
    # type: (List[int], int) -> List[int]
    '''
    Faster FFT for the second half of the input : the pattern for nth digit is [0]*(n-1) + [1]*n, so the output for nth
    digit is sum(sequence[n:]) % 10 and the output for the nth digit is (sequence[n] + output[n+1]) % 10
    '''
    for iter in range(0, iterations):
        value = 0
        for i in range(len(sequence) - 1, -1, -1): # Update the list in reverse order
            value = (sequence[i] + value) % 10
            sequence[i] = value
    return sequence

def calculate_d16p2(sequence):
    # type: (Text) -> Text
    '''
    This solution will only work if the offset is above the half of the message, as there is a way to fast compute the
    second half of each step, without computing the whole sequence.
    '''
    offset = int(sequence[0:7])
    if offset < 5000 * len(sequence):
        raise Exception("No fast solution for offset in the first half :(")
    sequence = (5000 * sequence)[offset - 5000 * len(sequence):] # Just need the message starting from the offset
    return ''.join(map(str, apply_fast_fft(list(map(int, sequence)), 100)[0:8]))

def run(with_tests = True):
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        sequence = in_file.readlines()[0].strip()

    if with_tests: checks_d16p1()

    d16p1 = apply_fft_with_fast_fft(sequence, 100)[0:8]
    print(f'Day 16, Part 1 : {d16p1}') # 90744714

    d16p2 = calculate_d16p2(sequence)
    print(f'Day 16, Part 2 : {d16p2}') # 82994322

if __name__ == '__main__':
    run()
