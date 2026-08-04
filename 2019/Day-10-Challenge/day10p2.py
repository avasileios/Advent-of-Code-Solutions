import os
import sys
from math import atan2, hypot


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])
    asteroids = [(x, y) for y in range(h) for x in range(w)
                 if grid[y][x] == '#']

    # find the station: the asteroid with maximum visible asteroids
    best_pos = None
    best_count = 0
    for x1, y1 in asteroids:
        angles = set()
        for x2, y2 in asteroids:
            if (x1, y1) == (x2, y2):
                continue
            angles.add(atan2(y2 - y1, x2 - x1))
        if len(angles) > best_count:
            best_count = len(angles)
            best_pos = (x1, y1)

    sx, sy = best_pos
    targets = []
    for x, y in asteroids:
        if (x, y) == (sx, sy):
            continue
        # angle measured clockwise from "up" (screen coords, y down):
        # up = 0, right = pi/2, down = pi, left = 3pi/2
        angle = atan2(x - sx, -(y - sy)) % (2 * 3.141592653589793)
        dist = hypot(x - sx, y - sy)
        targets.append((angle, dist, x, y))

    targets.sort()

    # vaporize: repeatedly take the closest asteroid of each distinct angle,
    # cycling through angles in order
    vaporized = []
    remaining = targets[:]
    while remaining:
        nxt = []
        last_angle = None
        for t in remaining:
            if t[0] != last_angle:
                vaporized.append(t)
                last_angle = t[0]
            else:
                nxt.append(t)
        remaining = nxt

    x200, y200 = vaporized[199][2], vaporized[199][3]
    print(x200 * 100 + y200)


if __name__ == "__main__":
    main()
