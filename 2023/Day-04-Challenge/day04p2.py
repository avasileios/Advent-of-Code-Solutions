import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    copies = [1] * len(lines)
    for i, line in enumerate(lines):
        _, rest = line.split(': ')
        a, b = rest.split(' | ')
        wins = set(int(x) for x in a.split())
        have = set(int(x) for x in b.split())
        matches = len(wins & have)
        for j in range(i + 1, min(i + 1 + matches, len(lines))):
            copies[j] += copies[i]
    print(sum(copies))


if __name__ == "__main__":
    main()
