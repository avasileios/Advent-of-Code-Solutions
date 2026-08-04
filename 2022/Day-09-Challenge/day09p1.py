import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    hx = hy = tx = ty = 0
    visited = {(0, 0)}
    for line in lines:
        d, n = line.split()
        n = int(n)
        for _ in range(n):
            if d == 'R':
                hx += 1
            elif d == 'L':
                hx -= 1
            elif d == 'U':
                hy += 1
            else:
                hy -= 1
            dx = hx - tx
            dy = hy - ty
            if abs(dx) > 1 or abs(dy) > 1:
                tx += (dx > 0) - (dx < 0)
                ty += (dy > 0) - (dy < 0)
            visited.add((tx, ty))
    print(len(visited))


if __name__ == "__main__":
    main()
