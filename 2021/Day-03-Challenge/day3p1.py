import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    n = len(lines)
    width = len(lines[0])
    counts = [0] * width
    for line in lines:
        for i, c in enumerate(line):
            if c == '1':
                counts[i] += 1

    gamma = 0
    epsilon = 0
    for i in range(width):
        if counts[i] > n // 2:
            gamma |= 1 << (width - 1 - i)
        else:
            epsilon |= 1 << (width - 1 - i)

    print(gamma * epsilon)


if __name__ == "__main__":
    main()
