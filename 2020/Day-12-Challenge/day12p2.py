import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    x = y = 0
    wx, wy = 10, -1  # waypoint relative to the ship
    for line in lines:
        c = line[0]
        n = int(line[1:])
        if c == 'N':
            wy -= n
        elif c == 'S':
            wy += n
        elif c == 'E':
            wx += n
        elif c == 'W':
            wx -= n
        elif c == 'L' or c == 'R':
            turns = (n // 90) % 4
            if c == 'L':
                turns = (4 - turns) % 4
            for _ in range(turns):
                wx, wy = -wy, wx  # rotate 90 clockwise
        elif c == 'F':
            x += wx * n
            y += wy * n

    print(abs(x) + abs(y))


if __name__ == "__main__":
    main()
