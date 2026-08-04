import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        edges = [tuple(line.strip().split('-')) for line in f if line.strip()]

    graph = {}
    for a, b in edges:
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, []).append(a)

    def dfs(node, visited):
        if node == 'end':
            return 1
        total = 0
        for nxt in graph[node]:
            if nxt.islower() and nxt in visited:
                continue
            new_visited = visited | {nxt} if nxt.islower() else visited
            total += dfs(nxt, new_visited)
        return total

    print(dfs('start', {'start'}))


if __name__ == "__main__":
    main()
