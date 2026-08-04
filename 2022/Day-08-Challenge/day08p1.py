import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [[int(c) for c in l.strip()] for l in f if l.strip()]

    h, w = len(grid), len(grid[0])
    visible = set()
    # from edges
    for y in range(h):
        m = -1
        for x in range(w):
            if grid[y][x] > m:
                visible.add((x, y))
                m = grid[y][x]
        m = -1
        for x in range(w - 1, -1, -1):
            if grid[y][x] > m:
                visible.add((x, y))
                m = grid[y][x]
    for x in range(w):
        m = -1
        for y in range(h):
            if grid[y][x] > m:
                visible.add((x, y))
                m = grid[y][x]
        m = -1
        for y in range(h - 1, -1, -1):
            if grid[y][x] > m:
                visible.add((x, y))
                m = grid[y][x]

    print(len(visible))


if __name__ == "__main__":
    main()
