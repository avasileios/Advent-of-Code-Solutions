import os
import sys


def count_removable(grid):
    h = len(grid)
    w = len(grid[0])
    removed = 0

    def accessible():
        cells = []
        for r in range(h):
            for c in range(w):
                if grid[r][c] != '@':
                    continue
                neigh = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] == '@':
                            neigh += 1
                if neigh < 4:
                    cells.append((r, c))
        return cells

    while True:
        cells = accessible()
        if not cells:
            break
        for r, c in cells:
            grid[r][c] = '.'
        removed += len(cells)

    return removed


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [list(line.strip()) for line in f if line.strip()]

    print(count_removable(grid))


if __name__ == "__main__":
    main()
