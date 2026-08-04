import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    parent = {}
    for line in lines:
        a, b = line.split(')')
        parent[b] = a

    total = 0
    for obj in parent:
        cur = obj
        while cur in parent:
            cur = parent[cur]
            total += 1

    print(total)


if __name__ == "__main__":
    main()
