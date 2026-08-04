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
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                counts[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                counts[(x, y1)] += 1

    print(sum(1 for v in counts.values() if v >= 2))


if __name__ == "__main__":
    main()
