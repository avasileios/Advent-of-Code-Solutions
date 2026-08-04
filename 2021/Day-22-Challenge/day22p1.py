import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    cuboids = []  # list of (x0, x1, y0, y1, z0, z1, on)
    for line in lines:
        m = re.match(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)', line)
        on = m.group(1) == 'on'
        x0, x1, y0, y1, z0, z1 = map(int, m.groups()[1:])
        # only the -50..50 region
        if x1 < -50 or x0 > 50 or y1 < -50 or y0 > 50 or z1 < -50 or z0 > 50:
            continue
        cuboids.append((x0, x1, y0, y1, z0, z1, on))

    lit = set()
    for x0, x1, y0, y1, z0, z1, on in cuboids:
        for x in range(max(x0, -50), min(x1, 50) + 1):
            for y in range(max(y0, -50), min(y1, 50) + 1):
                for z in range(max(z0, -50), min(z1, 50) + 1):
                    if on:
                        lit.add((x, y, z))
                    else:
                        lit.discard((x, y, z))

    print(len(lit))


if __name__ == "__main__":
    main()
