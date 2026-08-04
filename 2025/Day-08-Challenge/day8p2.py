import os
import sys


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

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
        self.components -= 1
        return True


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

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

    pairs = []
    for i in range(n):
        xi, yi, zi = points[i]
        for j in range(i + 1, n):
            xj, yj, zj = points[j]
            dx, dy, dz = xi - xj, yi - yj, zi - zj
            pairs.append((dx * dx + dy * dy + dz * dz, i, j))
    pairs.sort()

    for d2, i, j in pairs:
        if uf.union(i, j):
            if uf.components == 1:
                # last two junction boxes to connect
                print(points[i][0] * points[j][0])
                return


if __name__ == "__main__":
    main()
