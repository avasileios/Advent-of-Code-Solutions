import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    knots = [(0, 0)] * 10
    visited = {(0, 0)}
    for line in lines:
        d, n = line.split()
        n = int(n)
        for _ in range(n):
            hx, hy = knots[0]
            if d == 'R':
                hx += 1
            elif d == 'L':
                hx -= 1
            elif d == 'U':
                hy += 1
            else:
                hy -= 1
            knots[0] = (hx, hy)
            for i in range(1, 10):
                px, py = knots[i - 1]
                cx, cy = knots[i]
                dx = px - cx
                dy = py - cy
                if abs(dx) > 1 or abs(dy) > 1:
                    cx += (dx > 0) - (dx < 0)
                    cy += (dy > 0) - (dy < 0)
                knots[i] = (cx, cy)
            visited.add(knots[9])
    print(len(visited))


if __name__ == "__main__":
    main()
