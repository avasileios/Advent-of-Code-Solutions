import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    sections = data.split('\n\n')
    field_names = []
    field_ranges = []
    for line in sections[0].splitlines():
        m = re.match(r'([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)', line)
        field_names.append(m.group(1))
        field_ranges.append((int(m.group(2)), int(m.group(3)),
                             int(m.group(4)), int(m.group(5))))

    my_ticket = [int(x) for x in sections[1].splitlines()[1].split(',')]

    nearby = []
    for line in sections[2].splitlines()[1:]:
        nearby.append([int(x) for x in line.split(',')])

    # keep only valid tickets
    valid_tickets = []
    for ticket in nearby:
        if all(any(a <= v <= b or c <= v <= d
                   for a, b, c, d in field_ranges) for v in ticket):
            valid_tickets.append(ticket)

    nfields = len(field_names)
    # candidates[field] = set of possible positions
    candidates = []
    for fi in range(nfields):
        a, b, c, d = field_ranges[fi]
        pos = set()
        for p in range(nfields):
            if all((a <= t[p] <= b or c <= t[p] <= d)
                   for t in valid_tickets + [my_ticket]):
                pos.add(p)
        candidates.append(pos)

    # deduction: assign positions one at a time
    assigned = {}
    while len(assigned) < nfields:
        for fi in range(nfields):
            if fi not in assigned:
                remaining = candidates[fi] - set(assigned.values())
                if len(remaining) == 1:
                    assigned[fi] = remaining.pop()

    result = 1
    for fi, name in enumerate(field_names):
        if name.startswith('departure'):
            result *= my_ticket[assigned[fi]]

    print(result)


if __name__ == "__main__":
    main()
