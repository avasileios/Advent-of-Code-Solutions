import os
import sys


def step(grid):
    h = len(grid)
    w = len(grid[0])
    new = [row[:] for row in grid]
    for y in range(h):
        for x in range(w):
            n = 0
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == '#':
                    n += 1
            if grid[y][x] == '#':
                new[y][x] = '#' if n == 1 else '.'
            else:
                new[y][x] = '#' if 1 <= n <= 2 else '.'
    return new


def biodiversity(grid):
    total = 0
    flat = ''.join(''.join(row) for row in grid)
    for i, c in enumerate(flat):
        if c == '#':
            total += 2 ** i
    return total


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [list(line.strip()) for line in f if line.strip()]

    seen = set()
    while True:
        b = biodiversity(grid)
        if b in seen:
            print(b)
            return
        seen.add(b)
        grid = step(grid)


if __name__ == "__main__":
    main()
