import os
import sys
import heapq


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [[int(c) for c in line.strip()] for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])

    dist = {(0, 0): 0}
    pq = [(0, 0, 0)]
    while pq:
        d, x, y = heapq.heappop(pq)
        if (x, y) == (w - 1, h - 1):
            print(d)
            return
        if dist.get((x, y), 10**18) != d:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                nd = d + grid[ny][nx]
                if nd < dist.get((nx, ny), 10**18):
                    dist[(nx, ny)] = nd
                    heapq.heappush(pq, (nd, nx, ny))


if __name__ == "__main__":
    main()
