import os
import sys
from collections import deque

sys.setrecursionlimit(10000)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [l.rstrip('\n') for l in f]

    h, w = len(grid), len(grid[0])
    start = (grid[0].index('.'), 0)
    end = (grid[h - 1].index('.'), h - 1)

    # slopes force direction (part 1)
    slopes = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}

    # DFS with memo on (pos, visited) is too big; use longest-path DFS with
    # pruning via "remaining upper bound" - simpler: DFS with visited set
    best = 0
    visited = {start}

    def dfs(x, y, dist):
        nonlocal best
        if (x, y) == end:
            best = max(best, dist)
            return
        c = grid[y][x]
        if c in slopes:
            dx, dy = slopes[c]
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] != '#' and (nx, ny) not in visited:
                visited.add((nx, ny))
                dfs(nx, ny, dist + 1)
                visited.remove((nx, ny))
            return
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] != '#':
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    dfs(nx, ny, dist + 1)
                    visited.remove((nx, ny))

    dfs(start[0], start[1], 0)
    print(best)


if __name__ == "__main__":
    main()
