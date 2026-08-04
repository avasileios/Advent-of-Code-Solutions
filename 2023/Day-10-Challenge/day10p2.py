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

    def neighbors(x, y):
        result = []
        for dx, dy in pipes[grid[y][x]]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                nd = grid[ny][nx]
                if (-dx, -dy) in pipes[nd]:
                    result.append((nx, ny))
        return result

    # determine S's actual shape
    s_nbrs = neighbors(*start)
    s_dirs = [(nx - start[0], ny - start[1]) for nx, ny in s_nbrs]
    s_shape = None
    for ch, dirs in pipes.items():
        if ch != 'S' and sorted(dirs) == sorted(s_dirs):
            s_shape = ch
            break
    grid[start[1]] = grid[start[1]][:start[0]] + s_shape + grid[start[1]][start[0] + 1:]

    # walk the loop, collect vertices in order for shoelace
    pts = []
    x, y = start
    prev = None
    while True:
        pts.append((x, y))
        nbrs = neighbors(x, y)
        nxt = nbrs[0] if nbrs[0] != prev else nbrs[1]
        if nxt == start:
            break
        prev = (x, y)
        x, y = nxt

    # shoelace area
    n = len(pts)
    area2 = 0
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        area2 += x1 * y2 - x2 * y1
    area = abs(area2) // 2
    # Pick's theorem: interior = area - boundary/2 + 1
    interior = area - n // 2 + 1
    print(interior)


if __name__ == "__main__":
    main()
