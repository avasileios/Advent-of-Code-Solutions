import os
import sys


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

    # pipe connections: dirs where the pipe opens
    pipes = {
        '|': [(0, -1), (0, 1)],
        '-': [(-1, 0), (1, 0)],
        'L': [(0, -1), (1, 0)],
        'J': [(0, -1), (-1, 0)],
        '7': [(-1, 0), (0, 1)],
        'F': [(1, 0), (0, 1)],
        '.': [],
        'S': [(0, -1), (0, 1), (-1, 0), (1, 0)],
    }

    # find the two neighbors of S that connect back
    def neighbors(x, y):
        result = []
        for dx, dy in pipes[grid[y][x]]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                # does the neighbor connect back?
                nd = grid[ny][nx]
                if (-dx, -dy) in pipes[nd]:
                    result.append((nx, ny))
        return result

    # BFS along the loop
    dist = {start: 0}
    from collections import deque
    q = deque([start])
    while q:
        x, y = q.popleft()
        for nx, ny in neighbors(x, y):
            if (nx, ny) not in dist:
                dist[(nx, ny)] = dist[(x, y)] + 1
                q.append((nx, ny))

    print(max(dist.values()))


if __name__ == "__main__":
    main()
