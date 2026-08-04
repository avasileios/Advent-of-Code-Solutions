import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    sections = data.split('\n\n')
    fields = []
    for line in sections[0].splitlines():
        m = re.match(r'([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)', line)
        fields.append((int(m.group(2)), int(m.group(3)),
                       int(m.group(4)), int(m.group(5))))

    nearby = []
    for line in sections[2].splitlines()[1:]:
        nearby.append([int(x) for x in line.split(',')])

    total = 0
    for ticket in nearby:
        for v in ticket:
            if not any(a <= v <= b or c <= v <= d
                       for a, b, c, d in fields):
                total += v

    print(total)


if __name__ == "__main__":
    main()
