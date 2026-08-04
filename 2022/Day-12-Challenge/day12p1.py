import os
import sys
import heapq


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [l.strip() for l in f if l.strip()]

    h, w = len(grid), len(grid[0])
    start = end = None
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 'S':
                start = (x, y)
            elif grid[y][x] == 'E':
                end = (x, y)

    def elev(c):
        if c == 'S':
            return 0
        if c == 'E':
            return 25
        return ord(c) - ord('a')

    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, (x, y) = heapq.heappop(pq)
        if dist.get((x, y)) != d:
            continue
        if (x, y) == end:
            print(d)
            return
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if elev(grid[ny][nx]) <= elev(grid[y][x]) + 1:
                    nd = d + 1
                    if nd < dist.get((nx, ny), 10**18):
                        dist[(nx, ny)] = nd
                        heapq.heappush(pq, (nd, (nx, ny)))
    print(-1)


if __name__ == "__main__":
    main()
