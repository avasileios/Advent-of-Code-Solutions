import os
import sys
from collections import deque


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [[int(c) for c in line.strip()] for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])

    seen = set()
    basins = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 9 or (x, y) in seen:
                continue
            # BFS the basin
            size = 0
            q = deque([(x, y)])
            seen.add((x, y))
            while q:
                cx, cy = q.popleft()
                size += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen \
                            and grid[ny][nx] != 9:
                        seen.add((nx, ny))
                        q.append((nx, ny))
            basins.append(size)

    basins.sort(reverse=True)
    print(basins[0] * basins[1] * basins[2])


if __name__ == "__main__":
    main()
