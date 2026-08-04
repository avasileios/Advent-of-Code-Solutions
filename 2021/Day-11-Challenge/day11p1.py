import os
import sys


def step(grid, h, w):
    # increment all
    for y in range(h):
        for x in range(w):
            grid[y][x] += 1
    flashed = set()
    changed = True
    while changed:
        changed = False
        for y in range(h):
            for x in range(w):
                if grid[y][x] > 9 and (x, y) not in flashed:
                    flashed.add((x, y))
                    changed = True
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < h and 0 <= nx < w:
                                grid[ny][nx] += 1
    for x, y in flashed:
        grid[y][x] = 0
    return len(flashed)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [[int(c) for c in line.strip()] for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])
    total = 0
    for _ in range(100):
        total += step(grid, h, w)

    print(total)


if __name__ == "__main__":
    main()
