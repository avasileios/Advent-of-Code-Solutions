import os
import sys
from collections import deque


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [line.rstrip('\n') for line in f]

    h = len(grid)
    w = max(len(r) for r in grid)
    grid = [r.ljust(w) for r in grid]

    def is_letter(c):
        return 'A' <= c <= 'Z'

    # find portals: label -> walkable cell
    portal_cells = {}  # label -> list of (x, y)
    for y in range(h):
        for x in range(w):
            if not is_letter(grid[y][x]):
                continue
            # horizontal pair "AB"
            if x + 1 < w and is_letter(grid[y][x + 1]):
                label = grid[y][x] + grid[y][x + 1]
                # the walkable cell is to the left or right of the pair
                for cx, cy in ((x - 1, y), (x + 2, y)):
                    if 0 <= cx < w and 0 <= cy < h and grid[cy][cx] == '.':
                        portal_cells.setdefault(label, []).append((cx, cy))
            # vertical pair
            if y + 1 < h and is_letter(grid[y + 1][x]):
                label = grid[y][x] + grid[y + 1][x]
                for cx, cy in ((x, y - 1), (x, y + 2)):
                    if 0 <= cx < w and 0 <= cy < h and grid[cy][cx] == '.':
                        portal_cells.setdefault(label, []).append((cx, cy))

    start = portal_cells['AA'][0]
    target = portal_cells['ZZ'][0]

    # teleport map: cell -> other cell of the same portal
    teleport = {}
    for label, cells in portal_cells.items():
        if label in ('AA', 'ZZ'):
            continue
        if len(cells) == 2:
            teleport[cells[0]] = cells[1]
            teleport[cells[1]] = cells[0]

    # BFS
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        if (x, y) == target:
            print(dist[(x, y)])
            return
        nxt = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        if (x, y) in teleport:
            nxt.append(teleport[(x, y)])
        for nx, ny in nxt:
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == '.' \
                    and (nx, ny) not in dist:
                dist[(nx, ny)] = dist[(x, y)] + 1
                q.append((nx, ny))


if __name__ == "__main__":
    main()
