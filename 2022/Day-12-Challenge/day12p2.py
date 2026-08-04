import os
import sys
import heapq


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [l.strip() for l in f if l.strip()]

    h, w = len(grid), len(grid[0])
    end = None
    starts = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 'S':
                starts.append((x, y))
            elif grid[y][x] == 'E':
                end = (x, y)
            elif grid[y][x] == 'a':
                starts.append((x, y))

    def elev(c):
        if c == 'S':
            return 0
        if c == 'E':
            return 25
        return ord(c) - ord('a')

    # BFS from end going backwards (descent)
    dist = {end: 0}
    q = [end]
    from collections import deque
    q = deque([end])
    while q:
        x, y = q.popleft()
        d = dist[(x, y)]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if elev(grid[y][x]) <= elev(grid[ny][nx]) + 1:
                    if (nx, ny) not in dist:
                        dist[(nx, ny)] = d + 1
                        q.append((nx, ny))

    best = min(dist[s] for s in starts if s in dist)
    print(best)


if __name__ == "__main__":
    main()
