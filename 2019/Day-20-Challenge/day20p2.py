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

    def is_outer(x, y):
        return x <= 2 or y <= 2 or x >= w - 3 or y >= h - 3

    portal_cells = {}
    for y in range(h):
        for x in range(w):
            if not is_letter(grid[y][x]):
                continue
            if x + 1 < w and is_letter(grid[y][x + 1]):
                label = grid[y][x] + grid[y][x + 1]
                for cx, cy in ((x - 1, y), (x + 2, y)):
                    if 0 <= cx < w and 0 <= cy < h and grid[cy][cx] == '.':
                        portal_cells.setdefault(label, []).append(
                            (cx, cy, is_outer(cx, cy)))
            if y + 1 < h and is_letter(grid[y + 1][x]):
                label = grid[y][x] + grid[y + 1][x]
                for cx, cy in ((x, y - 1), (x, y + 2)):
                    if 0 <= cx < w and 0 <= cy < h and grid[cy][cx] == '.':
                        portal_cells.setdefault(label, []).append(
                            (cx, cy, is_outer(cx, cy)))

    start = portal_cells['AA'][0][:2]
    target = portal_cells['ZZ'][0][:2]

    teleport = {}
    for label, cells in portal_cells.items():
        if label in ('AA', 'ZZ') or len(cells) != 2:
            continue
        (x1, y1, o1), (x2, y2, o2) = cells
        teleport[(x1, y1)] = (x2, y2, o1)  # leaving (x1,y1) -> (x2,y2), level change: outer->+1? 
        teleport[(x2, y2)] = (x1, y1, o2)

    # BFS over (pos, level); AA/ZZ only usable at level 0.
    # Entering an inner portal goes to level+1; an outer portal to level-1.
    dist = {(start[0], start[1], 0): 0}
    q = deque([(start[0], start[1], 0)])
    while q:
        x, y, level = q.popleft()
        if (x, y) == target and level == 0:
            print(dist[(x, y, level)])
            return
        moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        if (x, y) in teleport:
            nx, ny, outer = teleport[(x, y)]
            if outer:
                # leaving an outer portal: go to level - 1
                nl = level - 1
            else:
                nl = level + 1
            if nl >= 0 and (nx, ny) != start and (nx, ny) != target:
                moves.append((nx, ny, nl))
        for m in moves:
            if len(m) == 3:
                nx, ny, nl = m
            else:
                nx, ny = m
                nl = level
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == '.' \
                    and (nx, ny, nl) not in dist:
                dist[(nx, ny, nl)] = dist[(x, y, level)] + 1
                q.append((nx, ny, nl))


if __name__ == "__main__":
    main()
