import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # bus i must depart at t + offset
    offsets = []
    for i, x in enumerate(lines[1].split(',')):
        if x != 'x':
            offsets.append((int(x), i))

    # Chinese remainder / incremental search:
    # t = -offset (mod bus) for each bus; combine one by one.
    t = 0
    step = 1
    for bus, offset in offsets:
        # find t such that (t + offset) % bus == 0
        while (t + offset) % bus != 0:
            t += step
        step *= bus

    print(t)


if __name__ == "__main__":
    main()
