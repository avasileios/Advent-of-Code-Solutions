import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        nums = [int(line) for line in f if line.strip()]

    sorted_nums = sorted(nums)
    jolts = [0] + sorted_nums + [sorted_nums[-1] + 3]

    diff1 = 0
    diff3 = 0
    for i in range(1, len(jolts)):
        d = jolts[i] - jolts[i - 1]
        if d == 1:
            diff1 += 1
        elif d == 3:
            diff3 += 1

    print(diff1 * diff3)


if __name__ == "__main__":
    main()
