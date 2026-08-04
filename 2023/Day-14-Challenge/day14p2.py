import os
import sys


def tilt(grid, dir):
    # dir: 0=N, 1=W, 2=S, 3=E
    h, w = len(grid), len(grid[0])
    if dir == 0:  # north
        for x in range(w):
            stop = 0
            for y in range(h):
                if grid[y][x] == 'O':
                    grid[y][x] = '.'
                    grid[stop][x] = 'O'
                    stop += 1
                elif grid[y][x] == '#':
                    stop = y + 1
    elif dir == 1:  # west
        for y in range(h):
            stop = 0
            for x in range(w):
                if grid[y][x] == 'O':
                    grid[y][x] = '.'
                    grid[y][stop] = 'O'
                    stop += 1
                elif grid[y][x] == '#':
                    stop = x + 1
    elif dir == 2:  # south
        for x in range(w):
            stop = h - 1
            for y in range(h - 1, -1, -1):
                if grid[y][x] == 'O':
                    grid[y][x] = '.'
                    grid[stop][x] = 'O'
                    stop -= 1
                elif grid[y][x] == '#':
                    stop = y - 1
    else:  # east
        for y in range(h):
            stop = w - 1
            for x in range(w - 1, -1, -1):
                if grid[y][x] == 'O':
                    grid[y][x] = '.'
                    grid[y][stop] = 'O'
                    stop -= 1
                elif grid[y][x] == '#':
                    stop = x - 1


def score(grid):
    h = len(grid)
    total = 0
    for y in range(h):
        for x in range(len(grid[y])):
            if grid[y][x] == 'O':
                total += h - y
    return total


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [list(l.strip()) for l in f if l.strip()]

    seen = {}
    cycle = 0
    target = 1000000000
    while cycle < target:
        for d in range(4):
            tilt(grid, d)
        cycle += 1
        key = tuple(tuple(r) for r in grid)
        if key in seen:
            prev = seen[key]
            period = cycle - prev
            remaining = target - cycle
            cycle += (remaining // period) * period
        else:
            seen[key] = cycle

    print(score(grid))


if __name__ == "__main__":
    main()
