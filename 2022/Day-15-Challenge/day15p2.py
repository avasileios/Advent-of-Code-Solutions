import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    sensors = []
    for line in lines:
        nums = list(map(int, re.findall(r'-?\d+', line)))
        sx, sy, bx, by = nums
        sensors.append((sx, sy, abs(sx - bx) + abs(sy - by)))

    LIMIT = 4000000
    for y in range(LIMIT + 1):
        intervals = []
        for sx, sy, d in sensors:
            dist_y = abs(sy - y)
            if dist_y <= d:
                reach = d - dist_y
                intervals.append((max(0, sx - reach), min(LIMIT, sx + reach)))
        if not intervals:
            continue
        intervals.sort()
        merged = [intervals[0]]
        for lo, hi in intervals[1:]:
            if lo <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
            else:
                merged.append((lo, hi))
        if len(merged) > 1:
            # gap between merged[0][1] and merged[1][0]
            x = merged[0][1] + 1
            print(x * LIMIT + y)
            return


if __name__ == "__main__":
    main()
