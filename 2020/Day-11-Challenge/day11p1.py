import os
import sys


def step(grid, h, w):
    new = [row[:] for row in grid]
    changed = False
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '.':
                continue
            n = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] == '#':
                        n += 1
            if grid[y][x] == 'L' and n == 0:
                new[y][x] = '#'
                changed = True
            elif grid[y][x] == '#' and n >= 4:
                new[y][x] = 'L'
                changed = True
    return new, changed


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [list(line.strip()) for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])
    while True:
        grid, changed = step(grid, h, w)
        if not changed:
            break

    print(sum(row.count('#') for row in grid))


if __name__ == "__main__":
    main()
