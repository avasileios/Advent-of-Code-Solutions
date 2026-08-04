import os
import sys
import re
from functools import lru_cache


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    flows = {}
    tunnels = {}
    for line in lines:
        m = re.match(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)', line)
        name, rate, dests = m.group(1), int(m.group(2)), m.group(3).split(', ')
        flows[name] = rate
        tunnels[name] = dests

    # Floyd-Warshall on all valves
    valves = list(flows.keys())
    n = len(valves)
    idx = {v: i for i, v in enumerate(valves)}
    INF = 10**9
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for v, dests in tunnels.items():
        for d in dests:
            dist[idx[v]][idx[d]] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # only valves with flow > 0
    useful = [v for v in valves if flows[v] > 0]
    m = len(useful)
    uidx = {v: i for i, v in enumerate(useful)}
    rates = [flows[v] for v in useful]
    start = idx['AA']

    @lru_cache(maxsize=None)
    def dfs(pos, time, mask):
        best = 0
        for i in range(m):
            if mask & (1 << i):
                d = dist[pos][idx[useful[i]]]
                if d + 1 <= time:
                    rem = time - d - 1
                    val = rates[i] * rem + dfs(idx[useful[i]], rem, mask & ~(1 << i))
                    best = max(best, val)
        return best

    print(dfs(start, 30, (1 << m) - 1))


if __name__ == "__main__":
    main()
