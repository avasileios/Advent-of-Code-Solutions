import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    total = 0
    for group in data.split('\n\n'):
        people = [set(p) for p in group.split()]
        common = set.intersection(*people) if people else set()
        total += len(common)

    print(total)


if __name__ == "__main__":
    main()
