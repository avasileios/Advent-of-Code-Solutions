import os
import sys
from collections import defaultdict


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    elves = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                elves.add((x, y))

    dirs = ['N', 'S', 'W', 'E']
    # checks for each direction
    checks = {
        'N': [(-1, -1), (0, -1), (1, -1)],
        'S': [(-1, 1), (0, 1), (1, 1)],
        'W': [(-1, -1), (-1, 0), (-1, 1)],
        'E': [(1, -1), (1, 0), (1, 1)],
    }
    move = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}
    all_adj = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    for round_no in range(10):
        proposals = {}
        counts = defaultdict(int)
        for x, y in elves:
            if all((x + dx, y + dy) not in elves for dx, dy in all_adj):
                continue
            for d in dirs:
                if all((x + dx, y + dy) not in elves for dx, dy in checks[d]):
                    nx, ny = x + move[d][0], y + move[d][1]
                    proposals[(x, y)] = (nx, ny)
                    counts[(nx, ny)] += 1
                    break
        new_elves = set()
        moved = False
        for e in elves:
            if e in proposals and counts[proposals[e]] == 1:
                new_elves.add(proposals[e])
                moved = True
            else:
                new_elves.add(e)
        elves = new_elves
        dirs = dirs[1:] + dirs[:1]

    xs = [e[0] for e in elves]
    ys = [e[1] for e in elves]
    area = (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)
    print(area - len(elves))


if __name__ == "__main__":
    main()
