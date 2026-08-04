import os
import sys
from functools import lru_cache


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    graph = {}
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, _, targets = line.partition(':')
            name = name.strip()
            outs = [t.strip() for t in targets.split() if t.strip()]
            graph[name] = outs

    @lru_cache(maxsize=None)
    def count_paths(node):
        if node == 'out':
            return 1
        total = 0
        for nxt in graph.get(node, []):
            total += count_paths(nxt)
        return total

    print(count_paths('you'))


if __name__ == "__main__":
    main()
