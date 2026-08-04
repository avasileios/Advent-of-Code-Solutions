import os
import sys


def find_reflection(grid):
    h = len(grid)
    for i in range(1, h):
        top = grid[:i]
        bottom = grid[i:]
        size = min(len(top), len(bottom))
        diffs = 0
        for a, b in zip(top[-size:], reversed(bottom[:size])):
            diffs += sum(1 for x, y in zip(a, b) if x != y)
        if diffs == 1:
            return i
    return 0


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()

    total = 0
    for block in data.strip().split('\n\n'):
        grid = block.splitlines()
        r = find_reflection(grid)
        if r:
            total += 100 * r
            continue
        tg = [''.join(grid[y][x] for y in range(len(grid)))
              for x in range(len(grid[0]))]
        c = find_reflection(tg)
        total += c
    print(total)


if __name__ == "__main__":
    main()
