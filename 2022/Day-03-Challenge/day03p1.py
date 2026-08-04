import os
import sys


def priority(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    return ord(c) - ord('A') + 27


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    total = 0
    for line in lines:
        half = len(line) // 2
        a, b = line[:half], line[half:]
        common = set(a) & set(b)
        total += priority(common.pop())
    print(total)


if __name__ == "__main__":
    main()
