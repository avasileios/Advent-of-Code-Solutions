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


def step(moons):
    n = len(moons)
    for i in range(n):
        for j in range(i + 1, n):
            for axis in range(3):
                a = moons[i][0][axis]
                b = moons[j][0][axis]
                d = (a < b) - (a > b)
                moons[i][1][axis] += d
                moons[j][1][axis] -= d
    for m in moons:
        for axis in range(3):
            m[0][axis] += m[1][axis]


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        moons = parse_moons([line for line in f if line.strip()])

    for _ in range(1000):
        step(moons)

    total = 0
    for pos, vel in moons:
        pot = sum(abs(v) for v in pos)
        kin = sum(abs(v) for v in vel)
        total += pot * kin

    print(total)


if __name__ == "__main__":
    main()
