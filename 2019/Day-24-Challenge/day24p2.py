import os
import sys


def neighbors(level, x, y):
    """Yield (level, x, y) neighbours of cell (x, y) at 'level'."""
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if nx == 2 and ny == 2:
            # the centre: goes to the next level's ring
            if (x, y) == (1, 2):
                for i in range(5):
                    yield (level + 1, 0, i)
            elif (x, y) == (3, 2):
                for i in range(5):
                    yield (level + 1, 4, i)
            elif (x, y) == (2, 1):
                for i in range(5):
                    yield (level + 1, i, 0)
            elif (x, y) == (2, 3):
                for i in range(5):
                    yield (level + 1, i, 4)
        elif 0 <= nx < 5 and 0 <= ny < 5:
            yield (level, nx, ny)
        else:
            # edge: goes to the parent level next to its centre
            if nx < 0:
                yield (level - 1, 1, 2)
            elif nx >= 5:
                yield (level - 1, 3, 2)
            elif ny < 0:
                yield (level - 1, 2, 1)
            elif ny >= 5:
                yield (level - 1, 2, 3)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # levels: dict level -> set of bug cells
    levels = {0: set()}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                levels[0].add((x, y))

    for _ in range(200):
        # collect all cells that might change
        cells = set()
        for level, bugs in levels.items():
            for (x, y) in bugs:
                cells.add((level, x, y))
                for n in neighbors(level, x, y):
                    cells.add(n)
        new_levels = {}
        for (level, x, y) in cells:
            if (x, y) == (2, 2):
                continue
            bug = (x, y) in levels.get(level, set())
            cnt = sum(1 for n in neighbors(level, x, y)
                      if n[1:] in levels.get(n[0], set()))
            if bug:
                alive = cnt == 1
            else:
                alive = 1 <= cnt <= 2
            if alive:
                new_levels.setdefault(level, set()).add((x, y))
        levels = new_levels

    total = sum(len(bugs) for bugs in levels.values())
    print(total)


if __name__ == "__main__":
    main()
