import os
import sys
from collections import deque


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        cubes = [tuple(map(int, l.split(','))) for l in f if l.strip()]

    s = set(cubes)
    min_x = min(c[0] for c in cubes) - 1
    max_x = max(c[0] for c in cubes) + 1
    min_y = min(c[1] for c in cubes) - 1
    max_y = max(c[1] for c in cubes) + 1
    min_z = min(c[2] for c in cubes) - 1
    max_z = max(c[2] for c in cubes) + 1

    # BFS through air from outside
    outside = set()
    q = deque([(min_x, min_y, min_z)])
    outside.add((min_x, min_y, min_z))
    while q:
        x, y, z = q.popleft()
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            nx, ny, nz = x + dx, y + dy, z + dz
            if min_x <= nx <= max_x and min_y <= ny <= max_y and min_z <= nz <= max_z:
                if (nx, ny, nz) not in s and (nx, ny, nz) not in outside:
                    outside.add((nx, ny, nz))
                    q.append((nx, ny, nz))

    total = 0
    for x, y, z in cubes:
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            if (x + dx, y + dy, z + dz) in outside:
                total += 1
    print(total)


if __name__ == "__main__":
    main()
