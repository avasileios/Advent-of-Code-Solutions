import os
import sys


def fuel_for(mass):
    f = mass // 3 - 2
    return max(f, 0)


def total_fuel(mass):
    total = 0
    while mass > 0:
        mass = fuel_for(mass)
        total += mass
    return total


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        masses = [int(line.strip()) for line in f if line.strip()]

    print(sum(total_fuel(m) for m in masses))


if __name__ == "__main__":
    main()
