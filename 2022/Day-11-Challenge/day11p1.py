import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()

    monkeys = []
    for block in data.strip().split('\n\n'):
        lines = block.splitlines()
        items = list(map(int, re.findall(r'\d+', lines[1])))
        op = lines[2].split('= ')[1]
        div = int(lines[3].split()[-1])
        t = int(lines[4].split()[-1])
        f = int(lines[5].split()[-1])
        monkeys.append({'items': items, 'op': op, 'div': div, 't': t, 'f': f, 'count': 0})

    for _ in range(20):
        for m in monkeys:
            for item in m['items']:
                m['count'] += 1
                old = item
                new = eval(m['op'])
                new //= 3
                if new % m['div'] == 0:
                    monkeys[m['t']]['items'].append(new)
                else:
                    monkeys[m['f']]['items'].append(new)
            m['items'] = []

    counts = sorted((m['count'] for m in monkeys), reverse=True)
    print(counts[0] * counts[1])


if __name__ == "__main__":
    main()
