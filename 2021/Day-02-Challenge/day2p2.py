import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    x = depth = aim = 0
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cmd, n = line.split()
            n = int(n)
            if cmd == 'forward':
                x += n
                depth += aim * n
            elif cmd == 'down':
                aim += n
            elif cmd == 'up':
                aim -= n

    print(x * depth)


if __name__ == "__main__":
    main()
