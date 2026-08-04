import os
import sys
from collections import deque


class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        q = deque([s])
        self.level[s] = 0
        while q:
            u = q.popleft()
            for v, cap, rev in self.graph[u]:
                if cap > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] >= 0

    def dfs(self, u, t, f):
        if u == t:
            return f
        for i in range(self.it[u], len(self.graph[u])):
            self.it[u] = i
            v, cap, rev = self.graph[u][i]
            if cap > 0 and self.level[v] == self.level[u] + 1:
                ret = self.dfs(v, t, min(f, cap))
                if ret > 0:
                    self.graph[u][i][1] -= ret
                    self.graph[v][rev][1] += ret
                    return ret
        return 0

    def max_flow(self, s, t):
        flow = 0
        INF = 10**9
        while self.bfs(s, t):
            self.it = [0] * self.n
            while True:
                f = self.dfs(s, t, INF)
                if f == 0:
                    break
                flow += f
                if flow > 100:
                    return flow
        return flow

    def reachable(self, s):
        seen = {s}
        q = deque([s])
        while q:
            u = q.popleft()
            for v, cap, rev in self.graph[u]:
                if cap > 0 and v not in seen:
                    seen.add(v)
                    q.append(v)
        return seen


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    edges = set()
    nodes = set()
    for line in lines:
        a, rest = line.split(': ')
        nodes.add(a)
        for b in rest.split():
            nodes.add(b)
            edges.add(tuple(sorted((a, b))))

    nodes = sorted(nodes)
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)

    s = 0
    for t in range(1, n):
        din = Dinic(n)
        for a, b in edges:
            din.add_edge(idx[a], idx[b], 1)
            din.add_edge(idx[b], idx[a], 1)
        flow = din.max_flow(s, t)
        if flow == 3:
            reach = din.reachable(s)
            a = len(reach)
            b = n - a
            print(a * b)
            return

    print("not found")


if __name__ == "__main__":
    main()
