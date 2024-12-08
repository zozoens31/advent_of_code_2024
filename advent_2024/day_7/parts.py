from collections.abc import Iterator
import sys
from typing import Literal


def parse_input(input_file) -> Iterator[tuple[int, list[int]]]:
    with open(input_file, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    for line in lines:
        total, rest = line.split(":", 1)
        yield int(total), [int(x) for x in rest.split(" ") if x]


def solve(
        total: int,
        numbers: list[int],
        with_concat: bool,
        expected_remain: Literal[0, 1, None] = None,
    ) -> bool | None:
    if total < 0:
        return None
    if not numbers:
        if (expected_remain == total):
            return True
        return None
    last = numbers[-1]
    start = numbers[:-1]
    if (not total % last) and solve(total // last, start, with_concat, 1):
        return True
    if not str(total).endswith(str(last)) or not with_concat:
        return solve(total - last, start, with_concat, 0)
    if last == total:
        return not start
    new_total_str = str(total).removesuffix(str(last))
    return (
        solve(int(new_total_str), start, with_concat) or
        solve(total - last, start, with_concat, 0)
    )


def main(input_file: str, with_concat: bool) -> int:
    return sum(
        total
        for total, numbers in parse_input(input_file)
        if solve(total, numbers, with_concat)
    )


if __name__ == "__main__":
    print(main(sys.argv[1], int(sys.argv[2])))
