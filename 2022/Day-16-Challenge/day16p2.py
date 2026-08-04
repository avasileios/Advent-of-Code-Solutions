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

    useful = [v for v in valves if flows[v] > 0]
    m = len(useful)
    uidx = {v: i for i, v in enumerate(useful)}
    rates = [flows[v] for v in useful]
    start = idx['AA']
    full = (1 << m) - 1

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

    # best flow per mask (exact) with 26 minutes
    f = [dfs(start, 26, mask) for mask in range(1 << m)]
    # g[mask] = max f[s] over subsets s of mask
    g = f[:]
    for i in range(m):
        for mask in range(1 << m):
            if mask & (1 << i):
                g[mask] = max(g[mask], g[mask ^ (1 << i)])

    ans = 0
    for mask in range(1 << m):
        ans = max(ans, f[mask] + g[full ^ mask])
    print(ans)


if __name__ == "__main__":
    main()
