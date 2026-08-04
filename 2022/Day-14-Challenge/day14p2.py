import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    rocks = set()
    for line in lines:
        pts = [tuple(map(int, p.split(','))) for p in line.split(' -> ')]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    rocks.add((x1, y))
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    rocks.add((x, y1))

    floor = max(y for _, y in rocks) + 2
    sand = set()
    while True:
        sx, sy = 500, 0
        while True:
            if sy + 1 == floor:
                sand.add((sx, sy))
                break
            if (sx, sy + 1) not in rocks and (sx, sy + 1) not in sand:
                sy += 1
            elif (sx - 1, sy + 1) not in rocks and (sx - 1, sy + 1) not in sand:
                sx -= 1
                sy += 1
            elif (sx + 1, sy + 1) not in rocks and (sx + 1, sy + 1) not in sand:
                sx += 1
                sy += 1
            else:
                sand.add((sx, sy))
                break
        if (500, 0) in sand:
            print(len(sand))
            return


if __name__ == "__main__":
    main()
