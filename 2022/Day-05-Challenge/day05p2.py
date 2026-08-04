import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.rstrip('\n') for l in f]

    idx = 0
    stacks = []
    while lines[idx].strip() and not lines[idx].strip().startswith('1'):
        row = lines[idx]
        n = (len(row) + 1) // 4
        while len(stacks) < n:
            stacks.append([])
        for i in range(n):
            c = row[1 + i * 4]
            if c != ' ':
                stacks[i].insert(0, c)
        idx += 1
    idx += 2

    for line in lines[idx:]:
        if not line.strip():
            continue
        m = re.match(r'move (\d+) from (\d+) to (\d+)', line)
        n, frm, to = map(int, m.groups())
        moved = stacks[frm - 1][-n:]
        stacks[frm - 1] = stacks[frm - 1][:-n]
        stacks[to - 1].extend(moved)

    print(''.join(s[-1] for s in stacks))


if __name__ == "__main__":
    main()
