import os
import sys
from math import atan2


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])
    asteroids = [(x, y) for y in range(h) for x in range(w)
                 if grid[y][x] == '#']

    best = 0
    for x1, y1 in asteroids:
        angles = set()
        for x2, y2 in asteroids:
            if (x1, y1) == (x2, y2):
                continue
            angles.add(atan2(y2 - y1, x2 - x1))
        best = max(best, len(angles))

    print(best)


if __name__ == "__main__":
    main()
