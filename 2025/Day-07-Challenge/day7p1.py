import os
import sys
from collections import deque


def simulate(grid):
    h = len(grid)
    w = len(grid[0])
    start_col = grid[0].index('S')

    splits = 0
    visited = set()
    queue = deque()

    def spawn(r, c):
        nonlocal splits
        if not (0 <= r < h and 0 <= c < w):
            return
        if (r, c) in visited:
            return
        visited.add((r, c))
        if grid[r][c] == '^':
            splits += 1
            spawn(r, c - 1)
            spawn(r, c + 1)
        else:
            queue.append((r, c))

    spawn(0, start_col)

    while queue:
        r, c = queue.popleft()
        nr = r + 1
        if nr >= h:
            continue  # beam exits the manifold
        spawn(nr, c)

    return splits


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [line.rstrip('\n') for line in f if line.strip()]

    print(simulate(grid))


if __name__ == "__main__":
    main()
