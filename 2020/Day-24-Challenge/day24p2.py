import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    dirs = {
        'e': (1, 0),
        'w': (-1, 0),
        'ne': (1, -1),
        'sw': (-1, 1),
        'se': (0, 1),
        'nw': (0, -1),
    }

    black = set()
    for line in lines:
        x = y = 0
        i = 0
        while i < len(line):
            if line[i] in 'ew':
                d = line[i]
                i += 1
            else:
                d = line[i:i + 2]
                i += 2
            dx, dy = dirs[d]
            x += dx
            y += dy
        pos = (x, y)
        if pos in black:
            black.discard(pos)
        else:
            black.add(pos)

    for _ in range(100):
        # cells to check: black cells + their neighbours
        cells = set()
        for (x, y) in black:
            cells.add((x, y))
            for dx, dy in dirs.values():
                cells.add((x + dx, y + dy))
        new_black = set()
        for (x, y) in cells:
            n = sum(1 for dx, dy in dirs.values()
                    if (x + dx, y + dy) in black)
            if (x, y) in black:
                if n == 1 or n == 2:
                    new_black.add((x, y))
            else:
                if n == 2:
                    new_black.add((x, y))
        black = new_black

    print(len(black))


if __name__ == "__main__":
    main()
