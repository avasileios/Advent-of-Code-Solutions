import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    valid = 0
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            policy, password = line.split(': ')
            rng, letter = policy.split(' ')
            a, b = map(int, rng.split('-'))
            if (password[a - 1] == letter) != (password[b - 1] == letter):
                valid += 1

    print(valid)


if __name__ == "__main__":
    main()
