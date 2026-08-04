import os
import sys
import math


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    t = int(''.join(lines[0].split(':')[1].split()))
    d = int(''.join(lines[1].split(':')[1].split()))

    # solve hold*(t-hold) > d: hold^2 - t*hold + d < 0
    disc = t * t - 4 * d
    lo = (t - math.sqrt(disc)) / 2
    hi = (t + math.sqrt(disc)) / 2
    # first integer strictly greater than lo, last strictly less than hi
    lo_i = int(lo) + 1
    hi_i = int(hi)
    if hi_i * (t - hi_i) <= d:
        hi_i -= 1
    print(hi_i - lo_i + 1)


if __name__ == "__main__":
    main()
