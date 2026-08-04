import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        nums = [int(x) for x in f.read().strip().split(',')]

    turns = 30000000
    last = {}
    for i, n in enumerate(nums[:-1]):
        last[n] = i

    prev = nums[-1]
    for i in range(len(nums) - 1, turns - 1):
        if prev in last:
            nxt = i - last[prev]
        else:
            nxt = 0
        last[prev] = i
        prev = nxt

    print(prev)


if __name__ == "__main__":
    main()
