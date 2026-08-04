import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    bricks = []
    for line in lines:
        a, b = line.split('~')
        x1, y1, z1 = map(int, a.split(','))
        x2, y2, z2 = map(int, b.split(','))
        bricks.append((x1, y1, z1, x2, y2, z2))
    bricks.sort(key=lambda b: min(b[2], b[5]))

    def overlaps(a, b):
        return a[0] <= b[3] and b[0] <= a[3] and a[1] <= b[4] and b[1] <= a[4]

    # settle
    settled = []
    supports = {}  # i -> set of supporting indices
    for i, (x1, y1, z1, x2, y2, z2) in enumerate(bricks):
        lo = min(z1, z2)
        # find highest settled brick below that overlaps in xy
        below = [j for j, s in enumerate(settled) if s[5] < lo and overlaps(s, (x1, y1, 0, x2, y2, 0))]
        top_z = max((settled[j][5] for j in below), default=0)
        nz1 = top_z + 1
        nz2 = nz1 + (z2 - z1)
        settled.append((x1, y1, nz1, x2, y2, nz2))
        sup = {j for j in below if settled[j][5] == top_z}
        supports[i] = sup

    needed = set()
    for sup in supports.values():
        if len(sup) == 1:
            needed.add(next(iter(sup)))
    print(len(settled) - len(needed))


if __name__ == "__main__":
    main()
