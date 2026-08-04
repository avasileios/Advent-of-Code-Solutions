import os
import sys
from collections import defaultdict


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    counts = defaultdict(int)
    for line in lines:
        x1, y1, x2, y2 = (int(v) for v in line.replace(' -> ', ',').split(','))
        dx = 1 if x2 > x1 else (-1 if x2 < x1 else 0)
        dy = 1 if y2 > y1 else (-1 if y2 < y1 else 0)
        x, y = x1, y1
        while True:
            counts[(x, y)] += 1
            if (x, y) == (x2, y2):
                break
            x += dx
            y += dy

    print(sum(1 for v in counts.values() if v >= 2))


if __name__ == "__main__":
    main()
