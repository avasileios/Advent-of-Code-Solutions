import os
import sys
from collections import deque


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

    settled = []
    supports = {}
    for i, (x1, y1, z1, x2, y2, z2) in enumerate(bricks):
        lo = min(z1, z2)
        below = [j for j, s in enumerate(settled) if s[5] < lo and overlaps(s, (x1, y1, 0, x2, y2, 0))]
        top_z = max((settled[j][5] for j in below), default=0)
        nz1 = top_z + 1
        nz2 = nz1 + (z2 - z1)
        settled.append((x1, y1, nz1, x2, y2, nz2))
        supports[i] = {j for j in below if settled[j][5] == top_z}

    n = len(settled)
    # who supports whom: supported_by[i] = set
    # falling of i: chain reaction
    total = 0
    for i in range(n):
        # remove brick i; count how many others fall
        removed = {i}
        changed = True
        while changed:
            changed = False
            for j in range(n):
                if j in removed:
                    continue
                if supports[j] and supports[j].issubset(removed):
                    removed.add(j)
                    changed = True
        total += len(removed) - 1
    print(total)


if __name__ == "__main__":
    main()
