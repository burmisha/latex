#!/usr/bin/env python3

numbers = [4, 1, 2, 3]
assert len(numbers) >= 2


def get_two_max(numbers):
    max_1, max_2 = None, None  # max_1 is greatest, max_2 is second after greatest
    for num in numbers:
        if max_1 is None:
            max_1 = num
        elif max_2 is None:
            max_2 = num
            if max_2 > max_1:
                max_1, max_2 = max_2, max_1
        else:
            if max_1 <= num:
                max_1, max_2 = num, max_1
            elif max_1 > num > max_2:
                max_2 = num

    return max_1, max_2


print(get_two_max([1]))
print(get_two_max([1, 2]))
print(get_two_max([2, 1]))
print(get_two_max(numbers))
print(get_two_max(range(100000000)))  # works with generators



