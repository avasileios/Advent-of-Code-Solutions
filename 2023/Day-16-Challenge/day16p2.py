import os
import sys
from collections import deque


def count_from(grid, sx, sy, sd):
    h, w = len(grid), len(grid[0])
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    tile_map = {
        '.': lambda d: [d],
        '/': lambda d: [{0: 3, 1: 2, 2: 1, 3: 0}[d]],
        '\\': lambda d: [{0: 1, 1: 0, 2: 3, 3: 2}[d]],
        '|': lambda d: [d] if d in (1, 3) else [1, 3],
        '-': lambda d: [d] if d in (0, 2) else [0, 2],
    }
    seen = set()
    q = deque([(sx, sy, sd)])
    while q:
        x, y, d = q.popleft()
        if (x, y, d) in seen:
            continue
        seen.add((x, y, d))
        for nd in tile_map[grid[y][x]](d):
            nx, ny = x + dx[nd], y + dy[nd]
            if 0 <= nx < w and 0 <= ny < h:
                q.append((nx, ny, nd))
    return len(set((x, y) for x, y, d in seen))


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [l.rstrip('\n') for l in f]

    h, w = len(grid), len(grid[0])
    best = 0
    for x in range(w):
        best = max(best, count_from(grid, x, 0, 1))
        best = max(best, count_from(grid, x, h - 1, 3))
    for y in range(h):
        best = max(best, count_from(grid, 0, y, 0))
        best = max(best, count_from(grid, w - 1, y, 2))
    print(best)


if __name__ == "__main__":
    main()
