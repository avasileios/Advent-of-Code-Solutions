import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        nums = [int(line) for line in f if line.strip()]

    count = sum(1 for i in range(1, len(nums)) if nums[i] > nums[i - 1])
    print(count)


if __name__ == "__main__":
    main()
