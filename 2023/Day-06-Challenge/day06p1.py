import os
import sys
import re
from math import prod


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    times = list(map(int, lines[0].split(':')[1].split()))
    dists = list(map(int, lines[1].split(':')[1].split()))

    total = 1
    for t, d in zip(times, dists):
        ways = 0
        for hold in range(1, t):
            if hold * (t - hold) > d:
                ways += 1
        total *= ways
    print(total)


if __name__ == "__main__":
    main()
