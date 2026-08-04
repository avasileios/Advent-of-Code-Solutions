import os
import sys
import re


def volume(c):
    x0, x1, y0, y1, z0, z1 = c
    return (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)


def intersect(a, b):
    x0 = max(a[0], b[0])
    x1 = min(a[1], b[1])
    y0 = max(a[2], b[2])
    y1 = min(a[3], b[3])
    z0 = max(a[4], b[4])
    z1 = min(a[5], b[5])
    if x0 <= x1 and y0 <= y1 and z0 <= z1:
        return (x0, x1, y0, y1, z0, z1)
    return None


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # keep a list of disjoint "on" cuboids
    on_cuboids = []
    for line in lines:
        m = re.match(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)', line)
        on = m.group(1) == 'on'
        cub = tuple(map(int, m.groups()[1:]))

        # subtract the new cuboid from all existing ones
        new_list = []
        for existing in on_cuboids:
            inter = intersect(existing, cub)
            if inter is None:
                new_list.append(existing)
                continue
            # split the existing cuboid into up to 6 pieces around the
            # intersection
            x0, x1, y0, y1, z0, z1 = existing
            ix0, ix1, iy0, iy1, iz0, iz1 = inter
            if x0 < ix0:
                new_list.append((x0, ix0 - 1, y0, y1, z0, z1))
            if ix1 < x1:
                new_list.append((ix1 + 1, x1, y0, y1, z0, z1))
            if y0 < iy0:
                new_list.append((ix0, ix1, y0, iy0 - 1, z0, z1))
            if iy1 < y1:
                new_list.append((ix0, ix1, iy1 + 1, y1, z0, z1))
            if z0 < iz0:
                new_list.append((ix0, ix1, iy0, iy1, z0, iz0 - 1))
            if iz1 < z1:
                new_list.append((ix0, ix1, iy0, iy1, iz1 + 1, z1))
        on_cuboids = new_list
        if on:
            on_cuboids.append(cub)

    print(sum(volume(c) for c in on_cuboids))


if __name__ == "__main__":
    main()
