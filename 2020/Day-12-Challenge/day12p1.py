import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    x = y = 0
    # directions: 0=N, 1=E, 2=S, 3=W
    d = 1
    for line in lines:
        c = line[0]
        n = int(line[1:])
        if c == 'N':
            y -= n
        elif c == 'S':
            y += n
        elif c == 'E':
            x += n
        elif c == 'W':
            x -= n
        elif c == 'L':
            d = (d - n // 90) % 4
        elif c == 'R':
            d = (d + n // 90) % 4
        elif c == 'F':
            if d == 0:
                y -= n
            elif d == 1:
                x += n
            elif d == 2:
                y += n
            else:
                x -= n

    print(abs(x) + abs(y))


if __name__ == "__main__":
    main()
