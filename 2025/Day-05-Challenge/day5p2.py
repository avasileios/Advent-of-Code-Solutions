import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        content = f.read().strip().split('\n')

    ranges = []
    i = 0
    while i < len(content) and content[i].strip():
        a, b = content[i].split('-')
        ranges.append((int(a), int(b)))
        i += 1

    ranges.sort()
    merged = []
    for a, b in ranges:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))

    total = 0
    for a, b in merged:
        total += b - a + 1

    print(total)


if __name__ == "__main__":
    main()
