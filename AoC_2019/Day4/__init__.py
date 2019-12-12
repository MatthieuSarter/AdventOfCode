from typing import Text, List


def meets_criteria_1(password):
    # type: (int) -> bool
    '''
    Checks if a given password meets the criteria for part 1.
    '''
    password_str = f'{password:06d}'
    two_adjacent_digits_same = False
    never_decrease = True
    for i in range(0, len(password_str) - 1):
        if password_str[i] == password_str[i + 1]:
            two_adjacent_digits_same = True
        if int(password_str[i]) > int(password_str[i + 1]):
            never_decrease = False
            break
    return two_adjacent_digits_same and never_decrease


def meets_criteria_2(password):
    # type: (int) -> bool
    '''
    Checks if a given password meets the criteria for part 2.
    '''
    password_str = f'{password:06d}'
    two_adjacent_digits_same = False
    never_decrease = True
    for i in range(0, len(password_str) - 1):
        if password_str[i] == password_str[i + 1] and (
                i == len(password_str) - 2 or password_str[i] != password_str[i + 2]) and (
                i == 0 or password_str[i] != password_str[i - 1]):
            two_adjacent_digits_same = True
        if int(password_str[i]) > int(password_str[i + 1]):
            never_decrease = False
            break
    return two_adjacent_digits_same and never_decrease


def get_matching_passwords(min, max, meets_criteria):
    # type: (int, int, callable) -> List[int]
    '''
    Lists all the valid password within a range.
    '''
    return [password for password in range(min, max + 1) if meets_criteria(password)]

def checks_d4p1():
    results = {
        111111: True,
        223450: False,
        123789: False,
    }
    for value, result in results.items():
        assert meets_criteria_1(value) == result

def checks_d4p2():
    results = {
        112233: True,
        123444: False,
        111122: True,
    }
    for value, result in results.items():
        assert meets_criteria_2(value) == result

def run(with_tests = True):
    checks_d4p1()

    d4p1 = len(get_matching_passwords(145852, 616942, meets_criteria_1))
    print(f'Day 4, Part 1 : {d4p1}')  # 1767

    if with_tests: checks_d4p2()

    d4p2 = len(get_matching_passwords(145852, 616942, meets_criteria_2))
    print(f'Day 4, Part 2 : {d4p2}')  # 1192


if __name__ == '__main__':
    run()