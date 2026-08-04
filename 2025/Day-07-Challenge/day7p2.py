import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]

    h = len(grid)
    w = len(grid[0])
    start_col = grid[0].index('S')

    # ways[r][c] = number of distinct timelines (paths) that reach cell (r, c)
    ways = [[0] * w for _ in range(h)]
    ways[0][start_col] = 1

    for r in range(h):
        # phase 1: every splitter sends its timelines to BOTH sides
        # (the beams continue on the same row, left and right)
        for c in range(w):
            if grid[r][c] == '^' and ways[r][c]:
                for dc in (-1, 1):
                    nc = c + dc
                    if 0 <= nc < w:
                        ways[r][nc] += ways[r][c]
        # phase 2: every non-splitter beam moves straight down
        for c in range(w):
            if grid[r][c] != '^' and ways[r][c] and r + 1 < h:
                ways[r + 1][c] += ways[r][c]

    # every particle in the last row exits the manifold; a particle at a
    # splitter in the last row has already been split into its two sides
    total = 0
    for c in range(w):
        if grid[h - 1][c] != '^':
            total += ways[h - 1][c]

    print(total)


if __name__ == "__main__":
    main()
