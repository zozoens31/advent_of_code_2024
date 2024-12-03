
from itertools import zip_longest
import sys
from typing import Iterator


def parse_input(input_file: str) -> tuple[list[int], list[int]]:
    with open(input_file) as file:
        content_lines = file.readlines()
    first_list = second_list = ()
    for line in content_lines:
        a, b = line.split(' ', 1)
        first_list += (int(a.strip()),)
        second_list += (int(b.strip()),)
    return first_list, second_list


def find_diffs(first_list: list[int], second_list: list[int]) -> Iterator[int]:
    for first, second in zip_longest(first_list, second_list):
        yield abs(first - second)

def find_distance(diffs: Iterator[int]) -> int:
    return sum(d for d in diffs)

def main(input_file: str) -> int:
    input1, input2 = parse_input(input_file)
    return find_distance(find_diffs(sorted(input1), sorted(input2)))

if __name__ == "__main__":
    print(main(sys.argv[1]))