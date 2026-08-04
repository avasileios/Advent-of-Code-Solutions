import os
import sys


def count_trees(grid, right, down):
    h = len(grid)
    w = len(grid[0])
    x = 0
    trees = 0
    for y in range(0, h, down):
        if grid[y][x % w] == '#':
            trees += 1
        x += right
    return trees


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]

    print(count_trees(grid, 3, 1))


if __name__ == "__main__":
    main()
