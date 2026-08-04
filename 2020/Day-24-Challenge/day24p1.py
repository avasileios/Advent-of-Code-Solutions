import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # hex grid with cube coordinates; e = (1,-1,0)-ish flat layout:
    # use axial coordinates: e=(1,0), w=(-1,0), ne=(0,-1), sw=(0,1),
    # se=(1,-1), nw=(-1,1)
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

    print(len(black))


if __name__ == "__main__":
    main()
