import os
import sys
import heapq


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [[int(c) for c in l.strip()] for l in f if l.strip()]

    h, w = len(grid), len(grid[0])
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    start = (0, 0, -1, 0)
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, (x, y, dr, st) = heapq.heappop(pq)
        if dist.get((x, y, dr, st)) != d:
            continue
        if (x, y) == (w - 1, h - 1) and st >= 4:
            print(d)
            return
        for nd in range(4):
            if dr != -1 and (nd + 2) % 4 == dr:
                continue
            if nd == dr:
                if st >= 10:
                    continue
                nst = st + 1
            else:
                if dr != -1 and st < 4:
                    continue
                nst = 1
            nx, ny = x + dx[nd], y + dy[nd]
            if 0 <= nx < w and 0 <= ny < h:
                ndist = d + grid[ny][nx]
                nstate = (nx, ny, nd, nst)
                if ndist < dist.get(nstate, 10**18):
                    dist[nstate] = ndist
                    heapq.heappush(pq, (ndist, nstate))
    print(-1)


if __name__ == "__main__":
    main()
