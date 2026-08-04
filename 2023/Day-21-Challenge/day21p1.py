import os
import sys
from collections import deque


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [l.rstrip('\n') for l in f]

    h, w = len(grid), len(grid[0])
    start = None
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 'S':
                start = (x, y)

    # BFS with parity: count reachable cells at even distance <= 64
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        if dist[(x, y)] == 64:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] != '#':
                if (nx, ny) not in dist:
                    dist[(nx, ny)] = dist[(x, y)] + 1
                    q.append((nx, ny))

    print(sum(1 for d in dist.values() if d <= 64 and d % 2 == 0))


if __name__ == "__main__":
    main()
