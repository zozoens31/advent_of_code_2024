
import sys


Letter = str

def parse_input(input_file: str) -> list[list[Letter]]:
    with open(input_file) as file:
        return file.readlines()

def count_word_starting_at(start: tuple[int, int], word_search: list[list[Letter]], word: str = 'XMAS') -> int:
    x, y = start
    return (
        ''.join(word_search[x][y:]).startswith(word) +
        ''.join(word_search[x][y::-1]).startswith(word) +
        ''.join(word_search[a][y] for a in range(x, len(word_search))).startswith(word) +
        ''.join(word_search[a][y] for a in range(x, -1, -1)).startswith(word) +
        ''.join(word_search[x+a][y+a] for a in range(len(word_search)-x) if y+a < len(word_search[0])).startswith(word) +
        ''.join(word_search[x+a][y-a] for a in range(len(word_search)-x) if y-a >= 0).startswith(word) +
        ''.join(word_search[x-a][y-a] for a in range(x+1) if y-a >= 0).startswith(word) +
        ''.join(word_search[x-a][y+a] for a in range(x+1) if y+a < len(word_search[0])).startswith(word)
    )

def main(input_file) -> int:
    word_search = parse_input(input_file)
    return sum(
        count_word_starting_at((i,j), word_search, word='XMAS')
        for i in range(len(word_search))
        for j in range(len(word_search[i]))
        if word_search[i][j] == 'X'
        )

if __name__ == "__main__":
    print(main(sys.argv[1]))