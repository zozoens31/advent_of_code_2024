import sys

from advent_2024.day_2.part_1 import Report, is_safe, parse_input


def is_dampened_safe(report: Report) -> bool:
    if is_safe(report):
        return True
    for idx in range(len(report)):
        dampened = list(report)
        del dampened[idx]
        if is_safe(dampened):
            return True
    return False

            
def main(input_file: str) -> int:
    return sum(1 for report in parse_input(input_file) if is_dampened_safe(report))


if __name__ == "__main__":
    print(main(sys.argv[1]))