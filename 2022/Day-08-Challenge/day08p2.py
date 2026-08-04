import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        grid = [[int(c) for c in l.strip()] for l in f if l.strip()]

    h, w = len(grid), len(grid[0])
    best = 0
    for y in range(h):
        for x in range(w):
            v = grid[y][x]
            score = 1
            # up
            d = 0
            for yy in range(y - 1, -1, -1):
                d += 1
                if grid[yy][x] >= v:
                    break
            score *= d
            # down
            d = 0
            for yy in range(y + 1, h):
                d += 1
                if grid[yy][x] >= v:
                    break
            score *= d
            # left
            d = 0
            for xx in range(x - 1, -1, -1):
                d += 1
                if grid[y][xx] >= v:
                    break
            score *= d
            # right
            d = 0
            for xx in range(x + 1, w):
                d += 1
                if grid[y][xx] >= v:
                    break
            score *= d
            best = max(best, score)
    print(best)


if __name__ == "__main__":
    main()
