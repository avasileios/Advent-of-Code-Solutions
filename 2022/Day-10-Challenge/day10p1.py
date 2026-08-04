import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    x = 1
    cycle = 0
    strength = 0
    checks = {20, 60, 100, 140, 180, 220}

    def tick():
        nonlocal cycle, strength
        cycle += 1
        if cycle in checks:
            strength += cycle * x

    for line in lines:
        if line == 'noop':
            tick()
        else:
            tick()
            tick()
            x += int(line.split()[1])
    print(strength)


if __name__ == "__main__":
    main()
