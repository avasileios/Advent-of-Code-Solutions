import os
import sys


def rating(lines, width, prefer_most):
    candidates = lines[:]
    for i in range(width):
        ones = sum(1 for c in candidates if c[i] == '1')
        zeros = len(candidates) - ones
        keep = '1' if (ones >= zeros) == prefer_most else '0'
        candidates = [c for c in candidates if c[i] == keep]
        if len(candidates) == 1:
            break
    return int(candidates[0], 2)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    width = len(lines[0])
    oxygen = rating(lines, width, True)
    co2 = rating(lines, width, False)
    print(oxygen * co2)


if __name__ == "__main__":
    main()
