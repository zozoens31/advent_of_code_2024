from itertools import groupby
import sys
from typing import Mapping

from advent_2024.day_1.part_1 import parse_input

def prepare_second_input_format(second_input: list[int]) -> Mapping[int, int]:
    return {
        value: sum(1 for _ in elements)
        for value, elements in groupby(sorted(second_input))
    }

def get_local_similarity(input_value: int, prepared_dict: Mapping[int, int]) -> int:
    return input_value * prepared_dict.get(input_value, 0)

def main(input_file: str) -> int:
    first_input, second_input = parse_input(input_file)
    mapping = prepare_second_input_format(second_input)
    return sum(get_local_similarity(value, mapping) for value in first_input)


if __name__ == "__main__":
    print(main(sys.argv[1]))