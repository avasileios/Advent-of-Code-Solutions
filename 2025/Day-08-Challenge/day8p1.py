import os
import sys


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    connections_needed = 1000
    if len(sys.argv) > 2:
        connections_needed = int(sys.argv[2])

    with open(input_file, 'r') as f:
        points = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y, z = map(int, line.split(','))
            points.append((x, y, z))

    n = len(points)
    uf = UnionFind(n)

    # Sort all pairs by squared Euclidean distance
    pairs = []
    for i in range(n):
        xi, yi, zi = points[i]
        for j in range(i + 1, n):
            xj, yj, zj = points[j]
            dx, dy, dz = xi - xj, yi - yj, zi - zj
            d2 = dx * dx + dy * dy + dz * dz
            pairs.append((d2, i, j))
    pairs.sort()

    # Process pairs in order of increasing distance; pairs already in the
    # same circuit are no-ops. We process exactly connections_needed pairs
    # (counting the no-ops), as the problem asks for the N closest pairs.
    processed = 0
    for d2, i, j in pairs:
        uf.union(i, j)
        processed += 1
        if processed == connections_needed:
            break

    sizes = sorted((s for s in uf.size if uf.find(s) == s and uf.size[s] > 0), reverse=True)
    result = sizes[0] * sizes[1] * sizes[2]
    print(result)


if __name__ == "__main__":
    main()
