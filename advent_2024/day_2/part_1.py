
import sys
from typing import Iterator

type Report = tuple[int, ...]


def parse_input(input_file: str) -> Iterator[Report]:
    with open(input_file) as file:
        raw_reports = file.readlines()
    for raw_report in raw_reports:
        yield tuple(int(level) for level in raw_report.split(' '))

def is_safe(report: Report) -> bool:
    is_ascending: bool | None = None
    for previous_level, level in zip(report, report[1:]):
        if is_ascending is None:
            is_ascending = previous_level <= level
        elif is_ascending != (previous_level <= level):
            return False
        if not (1 <= abs(previous_level - level) <= 3):
            return False
    return True
        
            
def main(input_file: str) -> int:
    return sum(1 for report in parse_input(input_file) if is_safe(report))


if __name__ == "__main__":
    print(main(sys.argv[1]))