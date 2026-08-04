import os
import sys
from collections import defaultdict


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [l.rstrip('\n') for l in f]

    h, w = len(grid), len(grid[0])
    start = (grid[0].index('.'), 0)
    end = (grid[h - 1].index('.'), h - 1)

    # find junctions (cells with 3+ open neighbors)
    def neighbors(x, y):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] != '#':
                yield (nx, ny)

    junctions = {start, end}
    for y in range(h):
        for x in range(w):
            if grid[y][x] != '#' and sum(1 for _ in neighbors(x, y)) >= 3:
                junctions.add((x, y))

    # compress: edges between junctions
    graph = defaultdict(list)  # junction -> [(other, dist)]
    for j in junctions:
        for n in neighbors(*j):
            prev = j
            cur = n
            dist = 1
            while cur not in junctions:
                nxt = [m for m in neighbors(*cur) if m != prev][0]
                prev, cur = cur, nxt
                dist += 1
            graph[j].append((cur, dist))

    # longest path DFS
    best = 0
    visited = {start}

    def dfs(node, dist):
        nonlocal best
        if node == end:
            best = max(best, dist)
            return
        for nxt, d in graph[node]:
            if nxt not in visited:
                visited.add(nxt)
                dfs(nxt, dist + d)
                visited.remove(nxt)

    dfs(start, 0)
    print(best)


if __name__ == "__main__":
    main()
