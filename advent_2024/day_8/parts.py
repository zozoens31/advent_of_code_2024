from collections.abc import Mapping, Sequence
from itertools import groupby
import sys
from typing import Collection

type Position = tuple[int, int]
def parse_input(
    input_file: str
) -> tuple[Position, Mapping[str, Sequence[Position]]]:
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = [str(line.strip()) for line in file]
    size = len(lines), len(lines[0])
    antennas = [
        (letter, (i, j))
        for i, line in enumerate(lines)
        for j, letter in enumerate(line)
        if letter != '.'
    ]
    return size, {
        letter: [pos for _, pos in group]
        for letter, group in groupby(
            sorted(antennas, key=lambda x: x[0]),
            key=lambda x: x[0]
        )
    }

def get_in_line(
    pos1: Position,
    pos2: Position,
    max_size: Position,
    only_opposite: bool = False,
) -> Collection[int]:
    x1, y1 = pos1
    x2, y2 = pos2
    max_x, max_y = max_size
    return [
        (x1 - k * (x1 - x2), y1 - k * (y1 - y2))
        for k in (
            (2,) if only_opposite
            else range(max(max_x, max_y) + 1)
        )
    ]

def within_bounds(pos: Position, size: Position) -> bool:
    x, y = pos
    return 0 <= x < size[0] and 0 <= y < size[1]

def add_antinodes(
    node1: Position,
    node2: Position,
    size: Position,
    only_opposite: bool,
) -> set[Position]:
    return {
        opp
        for opp in [
            *get_in_line(node1, node2, size, only_opposite),
            *get_in_line(node2, node1, size, only_opposite),
        ]
        if within_bounds(opp, size)
    }

def main(input_file: str, part_2: bool) -> int:
    size, antennas = parse_input(input_file)
    antinodes = {
        antinode
        for _, nodes in antennas.items()
        for node1 in nodes
        for node2 in nodes
        if node1 != node2
        for antinode in add_antinodes(node1, node2, size, not part_2)
    }
    return len(antinodes)

print(main(sys.argv[1], int(sys.argv[2])))    