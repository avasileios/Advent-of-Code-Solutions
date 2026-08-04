import os
import sys
from collections import deque


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

    # the input is a special garden: straight open lines through the center.
    # BFS far enough and use quadratic interpolation.
    # 26501365 = 65 + 131 * 202300 (grid is 131x131, start at center 65,65)
    steps = 26501365
    n_cycles = steps // h  # 202300
    # simulate up to a few cycles to sample the parabola
    # BFS on infinite grid with modulo
    def count_at(total_steps):
        seen = {(start, 0)}
        dist = {start: 0}
        q = deque([start])
        while q:
            x, y = q.popleft()
            d = dist[(x, y)]
            if d == total_steps:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if grid[ny % h][nx % w] != '#':
                    if (nx, ny) not in dist:
                        dist[(nx, ny)] = d + 1
                        q.append((nx, ny))
        return sum(1 for d in dist.values() if d <= total_steps and d % 2 == total_steps % 2)

    # sample at 65 + 131*k for k=0,1,2
    s0 = count_at(65)
    s1 = count_at(65 + h)
    s2 = count_at(65 + 2 * h)
    # quadratic fit: f(n) = a*n^2 + b*n + c for n = cycle index
    # f(0)=s0, f(1)=s1, f(2)=s2
    c = s0
    a = (s2 - 2 * s1 + s0) // 2
    b = s1 - s0 - a
    n = n_cycles
    print(a * n * n + b * n + c)


if __name__ == "__main__":
    main()
