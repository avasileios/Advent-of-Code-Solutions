import os
import sys
from itertools import combinations


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [l.strip() for l in f if l.strip()]

    h, w = len(grid), len(grid[0])
    galaxies = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '#':
                galaxies.append((x, y))

    empty_rows = [y for y in range(h) if '#' not in grid[y]]
    empty_cols = [x for x in range(w) if all(grid[y][x] == '.' for y in range(h))]

    total = 0
    for (x1, y1), (x2, y2) in combinations(galaxies, 2):
        d = abs(x1 - x2) + abs(y1 - y2)
        for r in empty_rows:
            if min(y1, y2) < r < max(y1, y2):
                d += 1
        for c in empty_cols:
            if min(x1, x2) < c < max(x1, x2):
                d += 1
        total += d
    print(total)


if __name__ == "__main__":
    main()
