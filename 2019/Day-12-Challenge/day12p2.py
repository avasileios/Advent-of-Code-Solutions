import os
import sys
import re
import math


def parse_moons(lines):
    moons = []
    for line in lines:
        m = re.match(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line.strip())
        moons.append([[int(m.group(1)), int(m.group(2)), int(m.group(3))],
                      [0, 0, 0]])
    return moons


def axis_period(positions):
    """Period of one axis (position+velocity state repeats)."""
    n = len(positions)
    state0 = tuple(positions) + (0,) * n
    pos = list(positions)
    vel = [0] * n
    t = 0
    while True:
        for i in range(n):
            for j in range(i + 1, n):
                d = (pos[i] < pos[j]) - (pos[i] > pos[j])
                vel[i] += d
                vel[j] -= d
        for i in range(n):
            pos[i] += vel[i]
        t += 1
        if tuple(pos) + tuple(vel) == state0:
            return t


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        moons = parse_moons([line for line in f if line.strip()])

    periods = []
    for axis in range(3):
        periods.append(axis_period([m[0][axis] for m in moons]))

    print(math.lcm(*periods))


if __name__ == "__main__":
    main()
