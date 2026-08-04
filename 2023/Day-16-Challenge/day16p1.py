import os
import sys
from collections import deque


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [l.rstrip('\n') for l in f]

    h, w = len(grid), len(grid[0])
    # beam: position + direction; 0=R,1=D,2=L,3=U
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    # tile -> mapping of (incoming dir) -> outgoing dirs
    tile_map = {
        '.': lambda d: [d],
        '/': lambda d: [{0: 3, 1: 2, 2: 1, 3: 0}[d]],
        '\\': lambda d: [{0: 1, 1: 0, 2: 3, 3: 2}[d]],
        '|': lambda d: [d] if d in (1, 3) else [1, 3],
        '-': lambda d: [d] if d in (0, 2) else [0, 2],
    }

    seen = set()
    q = deque([(0, 0, 0)])
    while q:
        x, y, d = q.popleft()
        if (x, y, d) in seen:
            continue
        seen.add((x, y, d))
        for nd in tile_map[grid[y][x]](d):
            nx, ny = x + dx[nd], y + dy[nd]
            if 0 <= nx < w and 0 <= ny < h:
                q.append((nx, ny, nd))

    energized = set((x, y) for x, y, d in seen)
    print(len(energized))


if __name__ == "__main__":
    main()
