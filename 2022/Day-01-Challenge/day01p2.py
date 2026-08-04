import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()
    sums = [sum(int(x) for x in block.split()) for block in data.strip().split('\n\n')]
    print(sum(sorted(sums, reverse=True)[:3]))


if __name__ == "__main__":
    main()
