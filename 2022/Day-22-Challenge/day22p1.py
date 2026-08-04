import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()

    grid_part, instr_part = data.split('\n\n')
    grid = grid_part.split('\n')
    h = len(grid)
    w = max(len(r) for r in grid)
    grid = [r.ljust(w) for r in grid]

    # directions: 0=R, 1=D, 2=L, 3=U
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    x = grid[0].index('.')
    y = 0
    d = 0

    instrs = re.findall(r'\d+|[LR]', instr_part)
    for ins in instrs:
        if ins == 'L':
            d = (d - 1) % 4
        elif ins == 'R':
            d = (d + 1) % 4
        else:
            n = int(ins)
            for _ in range(n):
                nx, ny = x + dx[d], y + dy[d]
                # wrap
                if d == 0 or d == 2:  # horizontal
                    while not (0 <= nx < w and grid[ny][nx] != ' '):
                        nx = (nx + dx[d]) % w
                else:  # vertical
                    while not (0 <= ny < h and grid[ny][nx] != ' '):
                        ny = (ny + dy[d]) % h
                if grid[ny][nx] == '#':
                    break
                x, y = nx, ny

    print(1000 * (y + 1) + 4 * (x + 1) + d)


if __name__ == "__main__":
    main()
