import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [list(l.strip()) for l in f if l.strip()]

    h, w = len(grid), len(grid[0])
    # tilt north
    for x in range(w):
        stop = 0
        for y in range(h):
            if grid[y][x] == 'O':
                grid[y][x] = '.'
                grid[stop][x] = 'O'
                stop += 1
            elif grid[y][x] == '#':
                stop = y + 1

    total = 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 'O':
                total += h - y
    print(total)


if __name__ == "__main__":
    main()
