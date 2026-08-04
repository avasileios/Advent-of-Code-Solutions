import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        line = f.read().strip()

    m = re.match(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)', line)
    x1, x2, y1, y2 = map(int, m.groups())

    # the maximum height: with vy0 > 0, it comes back to y=0 with vy=-vy0-1;
    # the next step must land in [y1, y2]
    best = 0
    for vx0 in range(1, 500):
        for vy0 in range(-200, 500):
            x = y = 0
            vx, vy = vx0, vy0
            max_y = 0
            while x <= x2 and y >= y1:
                x += vx
                y += vy
                if vx > 0:
                    vx -= 1
                vy -= 1
                max_y = max(max_y, y)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    best = max(best, max_y)
                    break

    print(best)


if __name__ == "__main__":
    main()
