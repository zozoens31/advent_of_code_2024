import sys


def parse_input(
    input_file: str
) -> tuple[list[tuple[int, int]], list[list[int]]]:
    orderings: list[tuple[int, int]] = []
    pages: list[list[int]] = []
    with open(input_file, 'r') as file:
        for line in file.readlines():
            if '|' in line:
                try:
                    orderings.append(tuple(
                        int(r)
                        for r in line.strip().split('|')
                    ))
                except ValueError:
                    print(line)
            
            elif not line.strip():
                continue
            else:
                pages.append([
                    int(r)
                    for r in line.strip().split(',')
                ])
    return orderings, pages

def reorder_page(page: list[int], orderings: list[tuple[int, int]]) -> list[int]:
    page = list(page)
    while True:
        for a, b in orderings:
            if a not in page or b not in page:
                continue
            a, b = page.index(a), page.index(b)
            if a > b:
                page[a], page[b] = page[b], page[a]
                break
        else:
            break
    return page

def main(file_name: str, keep_ordered_str: str) -> int:
    keep_ordered = keep_ordered_str.lower() in ('true','1', 'part_1')
    orderings, pages = parse_input(file_name)
    return sum(
        ordered_page[len(page) // 2]
        for page in pages
        if (ordered_page := reorder_page(page, orderings))
        if keep_ordered == (ordered_page == page)
    )

print(main(*sys.argv[1:]))
