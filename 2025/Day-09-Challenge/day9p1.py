import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        points = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split(','))
            points.append((x, y))

    n = len(points)
    best = 0
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > best:
                best = area

    print(best)


if __name__ == "__main__":
    main()
