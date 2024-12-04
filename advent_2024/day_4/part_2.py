import sys
from advent_2024.day_4.part_1 import parse_input, Letter


def count_crosses_around(start: tuple[int, int], word_search: list[list[Letter]], word: str) -> bool:
    x, y = start
    reversed = ''.join(c for c in word[-1::-1])
    if x <= 0 or x >= len(word_search) - 1:
        return False
    if y <= 0 or y >= len(word_search[x]) - 1:
        return False
    cross_1 = ''.join((word_search[x-1][y-1], word_search[x][y], word_search[x+1][y+1]))
    cross_2 = ''.join((word_search[x-1][y+1], word_search[x][y], word_search[x+1][y-1]))
    return cross_1 in (word, reversed) and cross_2 in (word, reversed)
    

def main(input_file: str, word: str = 'MAS') -> int:
    word_search = parse_input(input_file)
    assert len(word) == 3
    return sum(
        count_crosses_around((i,j), word_search, word)
        for i in range(len(word_search))
        for j in range(len(word_search[i]))
        if word_search[i][j] == 'A'
        )

if __name__ == "__main__":
    print(main(*sys.argv[1:]))