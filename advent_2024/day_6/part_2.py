import sys

from advent_2024.day_6.part_1 import NoEscapeException, get_escape_length, parse_input


def main(input_file: str) -> int:
    solutions = 0
    with open(input_file, 'r', encoding='utf-8') as file:
        raw_input = [line.strip() for line in file.readlines()]
    # Resolve the guard's escape first.
    solved_state = parse_input(raw_input)
    get_escape_length(solved_state)
    for i, grid_point in enumerate(solved_state.grid):
        if not grid_point.is_visited:
            continue
        test_state = parse_input(raw_input)
        test_state.grid[i].is_block = True
        try:
            get_escape_length(test_state)
        except NoEscapeException:
            print(test_state.grid[i])
            solutions += 1
    return solutions


if __name__ == '__main__':
    print(main(sys.argv[1]))