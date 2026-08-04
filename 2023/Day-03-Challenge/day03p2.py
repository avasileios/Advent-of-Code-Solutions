import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.rstrip('\n') for l in f]

    h, w = len(lines), len(lines[0])
    gears = {}
    for y, line in enumerate(lines):
        for m in re.finditer(r'\d+', line):
            value = int(m.group())
            adj = set()
            for x in range(m.start(), m.end()):
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and lines[ny][nx] == '*':
                            adj.add((nx, ny))
            for g in adj:
                gears.setdefault(g, []).append(value)

    total = 0
    for g, vals in gears.items():
        if len(vals) == 2:
            total += vals[0] * vals[1]
    print(total)


if __name__ == "__main__":
    main()
