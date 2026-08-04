import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [list(line.strip()) for line in f if line.strip()]

    # active cells as a set of (x, y, z)
    active = set()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '#':
                active.add((x, y, 0))

    for _ in range(6):
        # collect all cells to check
        cells = set()
        for (x, y, z) in active:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        if dx == 0 and dy == 0 and dz == 0:
                            continue
                        cells.add((x + dx, y + dy, z + dz))
            cells.add((x, y, z))

        new_active = set()
        for (x, y, z) in cells:
            n = 0
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        if dx == 0 and dy == 0 and dz == 0:
                            continue
                        if (x + dx, y + dy, z + dz) in active:
                            n += 1
            if (x, y, z) in active:
                if n in (2, 3):
                    new_active.add((x, y, z))
            else:
                if n == 3:
                    new_active.add((x, y, z))
        active = new_active

    print(len(active))


if __name__ == "__main__":
    main()
