import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()

    wf_part, _ = data.split('\n\n')
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

    # ranges: dict key -> (lo, hi) inclusive
    total = 0

    def count(name, ranges):
        nonlocal total
        if name == 'R':
            return
        if name == 'A':
            prod = 1
            for lo, hi in ranges.values():
                prod *= max(0, hi - lo + 1)
            total += prod
            return
        for key, op, val, dest in workflows[name]:
            if key is None:
                count(dest, ranges)
                return
            lo, hi = ranges[key]
            if op == '>':
                take = (val + 1, hi)
                leave = (lo, val)
            else:
                take = (lo, val - 1)
                leave = (val, hi)
            if take[0] <= take[1]:
                new_ranges = dict(ranges)
                new_ranges[key] = take
                count(dest, new_ranges)
            if leave[0] <= leave[1]:
                ranges = dict(ranges)
                ranges[key] = leave
            else:
                return

    count('in', {k: (1, 4000) for k in 'xmas'})
    print(total)


if __name__ == "__main__":
    main()
