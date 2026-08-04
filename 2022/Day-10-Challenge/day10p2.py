import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    x = 1
    cycle = 0
    screen = []

    def tick():
        nonlocal cycle
        pos = cycle % 40
        screen.append('#' if abs(pos - x) <= 1 else '.')
        cycle += 1

    for line in lines:
        if line == 'noop':
            tick()
        else:
            tick()
            tick()
            x += int(line.split()[1])

    for r in range(6):
        print(''.join(screen[r * 40:(r + 1) * 40]))


if __name__ == "__main__":
    main()
