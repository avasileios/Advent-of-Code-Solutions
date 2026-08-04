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
            outs = [t.strip() for t in targets.split() if t.strip()]
            graph[name.strip()] = outs

    DAC = 1
    FFT = 2

    @lru_cache(maxsize=None)
    def count_paths(node, seen):
        if node == 'out':
            return 1 if seen == (DAC | FFT) else 0
        total = 0
        for nxt in graph.get(node, []):
            ns = seen
            if nxt == 'dac':
                ns |= DAC
            elif nxt == 'fft':
                ns |= FFT
            total += count_paths(nxt, ns)
        return total

    print(count_paths('svr', 0))


if __name__ == "__main__":
    main()
