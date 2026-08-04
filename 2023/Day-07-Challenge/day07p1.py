import os
import sys
from collections import Counter

ORDER = '23456789TJQKA'


def hand_type(hand):
    counts = sorted(Counter(hand).values(), reverse=True)
    if counts[0] == 5:
        return 6
    if counts[0] == 4:
        return 5
    if counts[0] == 3 and counts[1] == 2:
        return 4
    if counts[0] == 3:
        return 3
    if counts[0] == 2 and counts[1] == 2:
        return 2
    if counts[0] == 2:
        return 1
    return 0


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    hands = []
    for line in lines:
        hand, bid = line.split()
        hands.append((hand, int(bid)))

    hands.sort(key=lambda hb: (hand_type(hb[0]),
                               [ORDER.index(c) for c in hb[0]]))
    total = 0
    for i, (hand, bid) in enumerate(hands, 1):
        total += i * bid
    print(total)


if __name__ == "__main__":
    main()
