import os
import sys


def valid(n):
    s = str(n)
    if len(s) != 6:
        return False
    for i in range(5):
        if s[i] > s[i + 1]:
            return False
    # exactly one pair of identical adjacent digits (a longer run does not
    # count as a pair)
    i = 0
    while i < 6:
        j = i
        while j < 6 and s[j] == s[i]:
            j += 1
        if j - i == 2:
            return True
        i = j
    return False


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lo, hi = map(int, f.read().strip().split('-'))

    count = 0
    for n in range(lo, hi + 1):
        if valid(n):
            count += 1

    print(count)


if __name__ == "__main__":
    main()
