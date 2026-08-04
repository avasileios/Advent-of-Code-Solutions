import os
import sys
from collections import deque


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [[int(c) for c in line.strip()] for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])
    low_points = []
    for y in range(h):
        for x in range(w):
            v = grid[y][x]
            if all(y + dy < 0 or y + dy >= h or x + dx < 0 or x + dx >= w
                   or grid[y + dy][x + dx] > v
                   for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                low_points.append((x, y))

    print(sum(grid[y][x] + 1 for x, y in low_points))


if __name__ == "__main__":
    main()
