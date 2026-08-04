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
    checks = {
        'N': [(-1, -1), (0, -1), (1, -1)],
        'S': [(-1, 1), (0, 1), (1, 1)],
        'W': [(-1, -1), (-1, 0), (-1, 1)],
        'E': [(1, -1), (1, 0), (1, 1)],
    }
    move = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}
    all_adj = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    round_no = 0
    while True:
        round_no += 1
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
        if not proposals:
            print(round_no)
            return
        new_elves = set()
        for e in elves:
            if e in proposals and counts[proposals[e]] == 1:
                new_elves.add(proposals[e])
            else:
                new_elves.add(e)
        elves = new_elves
        dirs = dirs[1:] + dirs[:1]


if __name__ == "__main__":
    main()
