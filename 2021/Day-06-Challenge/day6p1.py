import os
import sys


def simulate(fish, days):
    buckets = [0] * 9
    for f in fish:
        buckets[f] += 1
    for _ in range(days):
        new = buckets[0]
        buckets = buckets[1:] + [0]
        buckets[6] += new
        buckets[8] += new
    return sum(buckets)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        fish = [int(x) for x in f.read().strip().split(',')]

    print(simulate(fish, 80))


if __name__ == "__main__":
    main()
