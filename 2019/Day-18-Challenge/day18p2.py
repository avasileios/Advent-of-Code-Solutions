import os
import sys
import heapq
from collections import deque


def solve_maze(grid, starts):
    h = len(grid)
    w = len(grid[0])
    keys = {}
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if 'a' <= c <= 'z':
                keys[c] = (x, y)

    key_index = {k: i for i, k in enumerate(sorted(keys))}
    total_keys = len(keys)
    full_mask = (1 << total_keys) - 1

    def bfs(src):
        dist = {src: (0, 0)}
        q = deque([src])
        while q:
            x, y = q.popleft()
            d, dm = dist[(x, y)]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                c = grid[ny][nx]
                if c == '#':
                    continue
                ndm = dm
                if c.isupper():
                    ndm |= 1 << key_index[c.lower()]
                if (nx, ny) not in dist:
                    dist[(nx, ny)] = (d + 1, ndm)
                    q.append((nx, ny))
        out = {}
        for k, pos in keys.items():
            if pos in dist:
                out[k] = dist[pos]
        return out

    graph = {}
    for s_i, s in enumerate(starts):
        graph[('@' + str(s_i),)] = {}
        for k, (d, dm) in bfs(s).items():
            graph[('@' + str(s_i),)][k] = (d, dm)
    for k, pos in keys.items():
        graph[(k,)] = {}
        for k2, (d, dm) in bfs(pos).items():
            if k2 != k:
                graph[(k,)][k2] = (d, dm)

    start_pos = tuple('@' + str(i) for i in range(len(starts)))
    heap = [(0, start_pos, 0)]
    seen = {(start_pos, 0): 0}

    while heap:
        cost, poss, mask = heapq.heappop(heap)
        if seen.get((poss, mask), 10**18) != cost:
            continue
        if mask == full_mask:
            return cost
        for r in range(len(poss)):
            pos = poss[r]
            for k2, (d, dm) in graph[(pos,)].items():
                ki = key_index[k2]
                if mask & (1 << ki):
                    continue
                if dm & ~mask:
                    continue
                new_mask = mask | (1 << ki)
                new_poss = list(poss)
                new_poss[r] = k2
                nc = cost + d
                key = (tuple(new_poss), new_mask)
                if nc < seen.get(key, 10**18):
                    seen[key] = nc
                    heapq.heappush(heap, (nc, tuple(new_poss), new_mask))
    return None


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f]

    # find the start and carve the four quadrants
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '@':
                sx, sy = x, y

    grid[sy][sx] = '#'
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        grid[sy + dy][sx + dx] = '#'
    starts = [(sx - 1, sy - 1), (sx + 1, sy - 1),
              (sx - 1, sy + 1), (sx + 1, sy + 1)]
    for sx2, sy2 in starts:
        grid[sy2][sx2] = '@'

    print(solve_maze(grid, starts))


if __name__ == "__main__":
    main()
