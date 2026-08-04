import os
import sys


def seat_id(code):
    row = 0
    col = 0
    for c in code[:7]:
        row = row * 2 + (1 if c == 'B' else 0)
    for c in code[7:]:
        col = col * 2 + (1 if c == 'R' else 0)
    return row * 8 + col


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        codes = [line.strip() for line in f if line.strip()]

    ids = sorted(seat_id(c) for c in codes)
    for i in range(1, len(ids)):
        if ids[i] - ids[i - 1] == 2:
            print(ids[i] - 1)
            return


if __name__ == "__main__":
    main()
