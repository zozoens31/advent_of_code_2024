

from collections.abc import Mapping
from dataclasses import dataclass
import sys
from typing import Literal

Direction = Literal['up', 'right', 'down', 'left']
_TURN_RIGHT_ORDER = ['up', 'right', 'down', 'left', 'up']
TURN_RIGHT: Mapping[Direction, Direction] = {
    a: b
    for a, b in zip(_TURN_RIGHT_ORDER, _TURN_RIGHT_ORDER[1:])
}

class EscapeException(Exception):
    pass


@dataclass(kw_only=True)
class GridPoint:
    up: "GridPoint | None" = None
    down: "GridPoint | None" = None
    left: "GridPoint | None" = None
    right: "GridPoint  | None" = None
    is_block: bool = False
    is_visited: bool = False


@dataclass(kw_only=True)
class Guard:
    position: GridPoint
    facing: Direction

    def move(self) -> None:
        self.position.is_visited = True
        next_point: GridPoint | None = getattr(self.position, self.facing)
        if not next_point:
            raise EscapeException()
        if next_point.is_block:
            self.facing = TURN_RIGHT[self.facing]
        else:
            self.position = next_point


@dataclass(frozen=True, kw_only=True)
class State:
    grid: list[GridPoint]
    guard: Guard


def parse_input(input_file: str) -> State:
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    all_lines: list[GridPoint] = []
    previous_line: list[GridPoint] = []
    previous_point: GridPoint | None = None
    guard: Guard | None = None
    for line in lines:
        current_line: list[GridPoint] = []
        for char, top_point in zip(line, previous_line or [None for _ in line]):
            grid_point = GridPoint(up=top_point, left=previous_point, is_block=char == '#')
            if top_point:
                top_point.down = grid_point
            if previous_point:
                previous_point.right = grid_point
            if char == '^':
                guard = Guard(position=grid_point, facing='up')
            current_line.append(grid_point)
            previous_point = grid_point
        all_lines.extend(current_line)
        previous_line = current_line
    if not guard:
        raise ValueError('No guard found in input')
    return State(grid=all_lines, guard=guard)


def main(state: State) -> int:
    try:
        for _ in range(4*sum(not p.is_block for p in state.grid)):
            state.guard.move()
    except EscapeException:
        pass
    return sum(point.is_visited for point in state.grid)


def check_input(input_file: str) -> State:
    state = parse_input(input_file)
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    grid_iter = iter(state.grid)
    for line in lines:
        for char in line:
            point = next(grid_iter)
            match char:
                case '#':
                    assert point.is_block
                case '^':
                    assert point is state.guard.position
                case _:
                    assert not point.is_block
                    assert point is not state.guard.position
    return state

if __name__ == '__main__':
    print(main(check_input(sys.argv[1])))