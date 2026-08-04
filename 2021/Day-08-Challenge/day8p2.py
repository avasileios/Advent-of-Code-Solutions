import os
import sys


def decode(signals, outputs):
    """Map each scrambled segment pattern to its digit."""
    by_len = {}
    for s in signals:
        by_len.setdefault(len(s), []).append(set(s))
    one = by_len[2][0]
    seven = by_len[3][0]
    four = by_len[4][0]
    eight = by_len[7][0]
    # 6-segment digits: 0, 6, 9
    six_segs = by_len[6]
    nine = next(s for s in six_segs if four <= s)
    zero = next(s for s in six_segs if s != nine and one <= s)
    six = next(s for s in six_segs if s != nine and s != zero)
    # 5-segment digits: 2, 3, 5
    five_segs = by_len[5]
    three = next(s for s in five_segs if one <= s)
    five = next(s for s in five_segs if s != three and s | one == nine)
    two = next(s for s in five_segs if s != three and s != five)

    mapping = {frozenset(s): d for d, s in enumerate(
        [zero, one, two, three, four, five, six, seven, eight, nine])}

    value = 0
    for o in outputs:
        value = value * 10 + mapping[frozenset(o)]
    return value


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total = 0
    for line in lines:
        left, right = line.split(' | ')
        total += decode(left.split(), right.split())

    print(total)


if __name__ == "__main__":
    main()
