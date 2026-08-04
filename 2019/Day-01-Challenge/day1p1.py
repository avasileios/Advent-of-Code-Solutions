import os
import sys


def fuel_for(mass):
    return max(mass // 3 - 2, 0)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        masses = [int(line.strip()) for line in f if line.strip()]

    total = sum(fuel_for(m) for m in masses)
    print(total)


if __name__ == "__main__":
    main()
