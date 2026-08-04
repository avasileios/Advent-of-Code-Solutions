import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        cubes = [tuple(map(int, l.split(','))) for l in f if l.strip()]

    s = set(cubes)
    total = 0
    for x, y, z in cubes:
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            if (x + dx, y + dy, z + dz) not in s:
                total += 1
    print(total)


if __name__ == "__main__":
    main()
