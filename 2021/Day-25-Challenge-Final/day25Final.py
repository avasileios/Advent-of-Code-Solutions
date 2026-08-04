import os
import sys


def step(grid, h, w):
    # east-facing first
    moved = False
    new = [row[:] for row in grid]
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '>' and grid[y][(x + 1) % w] == '.':
                new[y][x] = '.'
                new[y][(x + 1) % w] = '>'
                moved = True
    grid = new
    new = [row[:] for row in grid]
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 'v' and grid[(y + 1) % h][x] == '.':
                new[y][x] = '.'
                new[(y + 1) % h][x] = 'v'
                moved = True
    return new, moved


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [list(line.strip()) for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])
    steps = 0
    while True:
        steps += 1
        grid, moved = step(grid, h, w)
        if not moved:
            print(steps)
            return


if __name__ == "__main__":
    main()
