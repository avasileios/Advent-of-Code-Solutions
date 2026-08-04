import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    total = 0
    for line in lines:
        a, b = line.split(',')
        a1, a2 = map(int, a.split('-'))
        b1, b2 = map(int, b.split('-'))
        if a1 <= b2 and b1 <= a2:
            total += 1
    print(total)


if __name__ == "__main__":
    main()
