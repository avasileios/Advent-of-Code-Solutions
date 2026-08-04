import os
import sys


def walk(path):
    """Yield (x, y, steps) along the path starting from (0, 0)."""
    x = y = 0
    steps = 0
    for move in path.split(','):
        d = move[0]
        dist = int(move[1:])
        for _ in range(dist):
            if d == 'R':
                x += 1
            elif d == 'L':
                x -= 1
            elif d == 'U':
                y += 1
            elif d == 'D':
                y -= 1
            steps += 1
            yield x, y, steps


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        wire1 = f.readline().strip()
        wire2 = f.readline().strip()

    visited = {}
    for x, y, steps in walk(wire1):
        if (x, y) not in visited:
            visited[(x, y)] = steps

    best = None
    for x, y, steps in walk(wire2):
        if (x, y) in visited:
            d = abs(x) + abs(y)
            if best is None or d < best:
                best = d

    print(best)


if __name__ == "__main__":
    main()
