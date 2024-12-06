

from collections.abc import Mapping
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
import sys
from typing import Literal

Direction = Literal['up', 'right', 'down', 'left']
_TURN_RIGHT_ORDER = ['up', 'right', 'down', 'left', 'up']
TURN_RIGHT: Mapping[Direction, Direction] = {
    a: b
    for a, b in zip(_TURN_RIGHT_ORDER, _TURN_RIGHT_ORDER[1:])
}
_DIRECTION_CHAR = {
    direction: char
    for direction, char in zip(_TURN_RIGHT_ORDER, '^>v<')
}

class EscapeException(Exception):
    pass

class NoEscapeException(Exception):
    pass


@dataclass(kw_only=True)
class GridPoint:
    x: int
    y: int
    up: "GridPoint | None" = None
    down: "GridPoint | None" = None
    left: "GridPoint | None" = None
    right: "GridPoint  | None" = None
    is_block: bool = False
    is_visited: bool = False

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'


@dataclass(kw_only=True)
class Guard:
    position: GridPoint
    facing: Direction

    def move(self) -> str:
        self.position.is_visited = True
        next_point: GridPoint | None = getattr(self.position, self.facing)
        if not next_point:
            raise EscapeException()
        if next_point.is_block:
            self.facing = TURN_RIGHT[self.facing]
            return ''
        else:
            self.position = next_point
            return _DIRECTION_CHAR[self.facing]


@dataclass(frozen=True, kw_only=True)
class State:
    grid: list[GridPoint]
    guard: Guard


def make_point(x: int, y: int, top_point: GridPoint | None, left_point: GridPoint | None, is_block: bool) -> GridPoint:
    point = GridPoint(x=x, y=y,up=top_point, left=left_point, is_block=is_block)
    if top_point:
        top_point.down = point
    if left_point:
        left_point.right = point
    return point


def parse_input(raw_input: list[str]) -> State:
    all_lines: list[GridPoint] = []
    previous_line: list[GridPoint | None] = [None for _ in raw_input[0]]
    previous_point: GridPoint | None = None
    guard: Guard | None = None
    for row, line in enumerate(raw_input):
        current_line: list[GridPoint] = []
        for col, (char, top_point) in enumerate(zip(line, previous_line)):
            grid_point = make_point(row, col, top_point, previous_point, char == '#')
            if char == '^':
                guard = Guard(position=grid_point, facing='up')
            current_line.append(grid_point)
            previous_point = grid_point
        all_lines.extend(current_line)
        assert len(current_line) == len(line)
        assert len(previous_line) == len(line), (row, len(previous_line), len(line))
        previous_line = current_line
        previous_point = None
    if not guard:
        raise ValueError('No guard found in input')
    return State(grid=all_lines, guard=guard)


def get_escape_length(state: State) -> int:
    moves = ""
    try:
        for _ in range(4*sum(not p.is_block for p in state.grid)):
            moves += state.guard.move()
    except EscapeException:
        return sum(point.is_visited for point in state.grid)
    raise NoEscapeException('Guard did not escape')


def main(input_file: str) -> int:
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
    state = parse_input(lines)
    return get_escape_length(state)


if __name__ == '__main__':
    print(main(sys.argv[1]))