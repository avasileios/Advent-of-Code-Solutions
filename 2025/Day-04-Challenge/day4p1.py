import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])
    accessible = 0

    for r in range(h):
        for c in range(w):
            if grid[r][c] != '@':
                continue
            neighbours = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] == '@':
                        neighbours += 1
            if neighbours < 4:
                accessible += 1

    print(accessible)


if __name__ == "__main__":
    main()
