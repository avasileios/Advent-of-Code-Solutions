import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        banks = [line.strip() for line in f if line.strip()]

    total = 0
    for bank in banks:
        n = len(bank)
        best = 0
        for i in range(n):
            for j in range(i + 1, n):
                value = int(bank[i]) * 10 + int(bank[j])
                if value > best:
                    best = value
        total += best

    print(total)


if __name__ == "__main__":
    main()
