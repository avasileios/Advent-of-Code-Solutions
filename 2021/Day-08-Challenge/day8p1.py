import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    count = 0
    for line in lines:
        outputs = line.split(' | ')[1].split()
        for o in outputs:
            if len(o) in (2, 3, 4, 7):
                count += 1

    print(count)


if __name__ == "__main__":
    main()
