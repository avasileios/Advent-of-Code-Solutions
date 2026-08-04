import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()

    wf_part, parts_part = data.split('\n\n')
    workflows = {}
    for line in wf_part.splitlines():
        name, rest = line.split('{')
        rules = rest[:-1].split(',')
        parsed = []
        for r in rules:
            if ':' in r:
                cond, dest = r.split(':')
                key = cond[0]
                op = cond[1]
                val = int(cond[2:])
                parsed.append((key, op, val, dest))
            else:
                parsed.append((None, None, None, r))
        workflows[name] = parsed

    total = 0
    for line in parts_part.splitlines():
        vals = {}
        for kv in line[1:-1].split(','):
            k, v = kv.split('=')
            vals[k] = int(v)
        cur = 'in'
        while cur not in ('A', 'R'):
            for key, op, val, dest in workflows[cur]:
                if key is None:
                    cur = dest
                    break
                v = vals[key]
                ok = v > val if op == '>' else v < val
                if ok:
                    cur = dest
                    break
        if cur == 'A':
            total += sum(vals.values())
    print(total)


if __name__ == "__main__":
    main()
