import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    sensors = []
    beacons = set()
    for line in lines:
        nums = list(map(int, re.findall(r'-?\d+', line)))
        sx, sy, bx, by = nums
        sensors.append((sx, sy, abs(sx - bx) + abs(sy - by)))
        beacons.add((bx, by))

    target = 2000000
    covered = set()
    for sx, sy, d in sensors:
        dist_y = abs(sy - target)
        if dist_y <= d:
            reach = d - dist_y
            for x in range(sx - reach, sx + reach + 1):
                covered.add(x)

    # remove beacons on the target row
    for bx, by in beacons:
        if by == target and bx in covered:
            covered.remove(bx)

    print(len(covered))


if __name__ == "__main__":
    main()
