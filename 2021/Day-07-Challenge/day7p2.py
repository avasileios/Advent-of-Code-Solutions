import os
import sys


def fuel_cost(pos, target):
    total = 0
    for p in pos:
        d = abs(p - target)
        total += d * (d + 1) // 2
    return total


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        pos = [int(x) for x in f.read().strip().split(',')]

    # optimal target is near the mean
    mean = sum(pos) // len(pos)
    best = min(fuel_cost(pos, t) for t in range(mean - 2, mean + 3))
    print(best)


if __name__ == "__main__":
    main()
