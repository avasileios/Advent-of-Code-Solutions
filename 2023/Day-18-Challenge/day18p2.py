import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    x = y = 0
    pts = [(0, 0)]
    boundary = 0
    dirs = {'0': (1, 0), '1': (0, 1), '2': (-1, 0), '3': (0, -1)}
    for line in lines:
        _, _, color = line.split()
        hexv = color[2:-1]
        n = int(hexv[:-1], 16)
        d = hexv[-1]
        dx, dy = dirs[d]
        x += dx * n
        y += dy * n
        pts.append((x, y))
        boundary += n

    area2 = 0
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        area2 += x1 * y2 - x2 * y1
    area = abs(area2) // 2
    print(area + boundary // 2 + 1)


if __name__ == "__main__":
    main()
