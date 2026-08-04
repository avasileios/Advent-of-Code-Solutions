import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.rstrip('\n') for l in f]

    h, w = len(lines), len(lines[0])
    numbers = []  # (value, set of coords)
    for y, line in enumerate(lines):
        for m in re.finditer(r'\d+', line):
            coords = set()
            for x in range(m.start(), m.end()):
                coords.add((x, y))
            numbers.append((int(m.group()), coords))

    total = 0
    for value, coords in numbers:
        adj = set()
        for x, y in coords:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in coords:
                        c = lines[ny][nx]
                        if c != '.' and not c.isdigit():
                            adj.add((nx, ny))
        if adj:
            total += value
    print(total)


if __name__ == "__main__":
    main()
