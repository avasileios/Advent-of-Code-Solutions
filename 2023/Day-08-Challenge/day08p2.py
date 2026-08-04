import os
import sys
from math import gcd


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    instr = lines[0]
    nodes = {}
    for line in lines[1:]:
        name, rest = line.split(' = ')
        l, r = rest[1:-1].split(', ')
        nodes[name] = (l, r)

    starts = [n for n in nodes if n.endswith('A')]
    periods = []
    for s in starts:
        cur = s
        steps = 0
        i = 0
        seen = {}
        while True:
            if cur.endswith('Z'):
                periods.append(steps)
                break
            d = instr[i % len(instr)]
            cur = nodes[cur][0 if d == 'L' else 1]
            steps += 1
            i += 1
    lcm = 1
    for p in periods:
        lcm = lcm * p // gcd(lcm, p)
    print(lcm)


if __name__ == "__main__":
    main()
