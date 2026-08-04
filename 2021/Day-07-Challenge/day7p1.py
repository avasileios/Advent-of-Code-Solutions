import os
import sys


def fuel_cost(pos, target):
    return sum(abs(p - target) for p in pos)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        pos = [int(x) for x in f.read().strip().split(',')]

    pos.sort()
    median = pos[len(pos) // 2]
    print(fuel_cost(pos, median))


if __name__ == "__main__":
    main()
