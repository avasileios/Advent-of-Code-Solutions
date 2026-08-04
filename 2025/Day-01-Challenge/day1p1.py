import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    position = 50
    zeros = 0

    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
        if position == 0:
            zeros += 1

    print(zeros)


if __name__ == "__main__":
    main()
