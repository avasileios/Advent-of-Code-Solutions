import os
import sys
from collections import deque


def rotations(p):
    x, y, z = p
    return [
        (x, y, z), (x, -y, -z), (-x, y, -z), (-x, -y, z),
        (x, z, -y), (x, -z, y), (-x, z, y), (-x, -z, -y),
        (y, x, -z), (y, -x, z), (-y, x, z), (-y, -x, -z),
        (y, z, x), (y, -z, -x), (-y, z, -x), (-y, -z, x),
        (z, x, y), (z, -x, -y), (-z, x, -y), (-z, -x, y),
        (z, y, -x), (z, -y, x), (-z, y, x), (-z, -y, -x),
    ]


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    scanners = []
    for block in data.split('\n\n'):
        beacons = []
        for line in block.splitlines()[1:]:
            if line.strip():
                beacons.append(tuple(int(v) for v in line.split(',')))
        scanners.append(beacons)

    n = len(scanners)
    rotated = [[[rotations(b)[r] for b in scanners[i]]
                for r in range(24)] for i in range(n)]

    positions = {0: (0, 0, 0)}
    placed = {0}

    queue = deque([0])
    while queue:
        i = queue.popleft()
        bi = set(scanners[i])
        for j in range(n):
            if j in placed:
                continue
            found = False
            for r in range(24):
                offsets = {}
                for bx in bi:
                    for by in rotated[j][r]:
                        off = (bx[0] - by[0], bx[1] - by[1], bx[2] - by[2])
                        offsets[off] = offsets.get(off, 0) + 1
                        if offsets[off] >= 12:
                            found = True
                            break
                    if found:
                        break
                if found:
                    positions[j] = off
                    scanners[j] = [(off[0] + by[0], off[1] + by[1],
                                    off[2] + by[2]) for by in rotated[j][r]]
                    placed.add(j)
                    queue.append(j)
                    break

    # max manhattan distance between any two scanners
    best = 0
    plist = list(positions.values())
    for i in range(len(plist)):
        for j in range(i + 1, len(plist)):
            d = sum(abs(plist[i][k] - plist[j][k]) for k in range(3))
            best = max(best, d)

    print(best)


if __name__ == "__main__":
    main()
