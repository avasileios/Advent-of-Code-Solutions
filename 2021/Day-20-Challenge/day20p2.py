import os
import sys


def enhance(algo, lit, steps):
    bg = 0
    for _ in range(steps):
        xs = [p[0] for p in lit]
        ys = [p[1] for p in lit]
        x0, x1 = min(xs), max(xs)
        y0, y1 = min(ys), max(ys)
        new_lit = set()
        for y in range(y0 - 1, y1 + 2):
            for x in range(x0 - 1, x1 + 2):
                idx = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        idx <<= 1
                        px, py = x + dx, y + dy
                        if (px, py) in lit:
                            idx |= 1
                        elif not (x0 <= px <= x1 and y0 <= py <= y1):
                            # outside the known grid: the background
                            if bg == 1:
                                idx |= 1
                if algo[idx] == '#':
                    new_lit.add((x, y))
        lit = new_lit
        bg = 1 - bg if algo[0] == '#' else 0
    return lit


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    algo = lines[0]
    grid = [line for line in lines[1:] if line]

    lit = set()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '#':
                lit.add((x, y))

    print(len(enhance(algo, lit, 50)))


if __name__ == "__main__":
    main()
