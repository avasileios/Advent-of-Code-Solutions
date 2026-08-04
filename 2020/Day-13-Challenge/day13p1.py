import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    earliest = int(lines[0])
    buses = [int(x) for x in lines[1].split(',') if x != 'x']

    best = None
    best_wait = None
    for b in buses:
        wait = (b - earliest % b) % b
        if best_wait is None or wait < best_wait:
            best_wait = wait
            best = b

    print(best * best_wait)


if __name__ == "__main__":
    main()
