import os
import re

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.num_sets = n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            self.num_sets -= 1
            return True
        return False

def manhattan_4d(p1, p2):
    return sum(abs(a - b) for a, b in zip(p1, p2))

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    if not os.path.exists(file_path):
        return "Error: input.txt not found."

    points = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                points.append(tuple(map(int, line.strip().split(','))))

    n = len(points)
    dsu = DSU(n)

    # Compare all pairs (O(N^2))
    # For ~1000-1500 points, this takes less than a second
    for i in range(n):
        for j in range(i + 1, n):
            if manhattan_4d(points[i], points[j]) <= 3:
                dsu.union(i, j)

    return dsu.num_sets

if __name__ == "__main__":
    result = solve()
    print(f"Number of constellations: {result}")