import os
import sys
import bisect


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        content = f.read().strip().split('\n')

    # Fresh ingredient ID ranges until the blank line
    ranges = []
    i = 0
    while i < len(content) and content[i].strip():
        a, b = content[i].split('-')
        ranges.append((int(a), int(b)))
        i += 1
    i += 1  # skip blank line

    ids = [int(x) for x in content[i:] if x.strip()]

    # Merge overlapping ranges
    ranges.sort()
    merged = []
    for a, b in ranges:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))

    starts = [m[0] for m in merged]
    ends = [m[1] for m in merged]

    fresh = 0
    for x in ids:
        idx = bisect.bisect_right(starts, x) - 1
        if idx >= 0 and x <= ends[idx]:
            fresh += 1

    print(fresh)


if __name__ == "__main__":
    main()
