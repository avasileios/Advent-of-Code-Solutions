import os
import sys


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

    cur = 'AAA'
    steps = 0
    i = 0
    while cur != 'ZZZ':
        d = instr[i % len(instr)]
        cur = nodes[cur][0 if d == 'L' else 1]
        steps += 1
        i += 1
    print(steps)


if __name__ == "__main__":
    main()
