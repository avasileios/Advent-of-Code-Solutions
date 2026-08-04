import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    pos = 50
    zeros = 0
    for line in lines:
        direction = line[0]
        dist = int(line[1:])
        if direction == 'R':
            # clicks visit pos+1 ... pos+dist; zero when pos+k == 0 (mod 100)
            base = (100 - pos % 100) % 100
            if base == 0:
                base = 100
            if base <= dist:
                zeros += 1 + (dist - base) // 100
            pos = (pos + dist) % 100
        else:
            # clicks visit pos-1 ... pos-dist
            base = pos % 100
            if base == 0:
                base = 100
            if base <= dist:
                zeros += 1 + (dist - base) // 100
            pos = (pos - dist) % 100

    print(zeros)


if __name__ == "__main__":
    main()
