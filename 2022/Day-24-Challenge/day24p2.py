import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.rstrip('\n') for l in f]

    h = len(lines) - 2
    w = len(lines[0]) - 2
    blizzards = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c in '<>^v':
                dx = {'<': -1, '>': 1}.get(c, 0)
                dy = {'^': -1, 'v': 1}.get(c, 0)
                blizzards.append((x - 1, y - 1, dx, dy))

    start = (0, -1)
    end = (w - 1, h)

    def travel(starts, target, t0):
        positions = set(starts)
        t = t0
        while True:
            t += 1
            # occupied cells this minute
            occ = set()
            for bx, by, dx, dy in blizzards:
                if dx:
                    occ.add(((bx + dx * t) % w, by))
                else:
                    occ.add((bx, (by + dy * t) % h))
            new_pos = set()
            for x, y in positions:
                for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) == target:
                        return t
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in occ:
                        new_pos.add((nx, ny))
            for x, y in positions:
                if (x, y) == start:
                    new_pos.add(start)
                if (x, y) == end:
                    new_pos.add(end)
            positions = new_pos

    t1 = travel({start}, end, 0)
    t2 = travel({end}, start, t1)
    t3 = travel({start}, end, t2)
    print(t3)


if __name__ == "__main__":
    main()
