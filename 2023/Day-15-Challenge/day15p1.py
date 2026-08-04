import os
import sys


def hash_str(s):
    v = 0
    for c in s:
        v = ((v + ord(c)) * 17) % 256
    return v


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read().strip()

    total = 0
    for part in data.split(','):
        total += hash_str(part)
    print(total)


if __name__ == "__main__":
    main()
