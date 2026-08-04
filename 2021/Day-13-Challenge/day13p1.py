import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    dots = set()
    folds = []
    for line in lines:
        if line.startswith('fold'):
            axis, val = line.split()[-1].split('=')
            folds.append((axis, int(val)))
        elif line:
            x, y = map(int, line.split(','))
            dots.add((x, y))

    # first fold only
    axis, val = folds[0]
    new_dots = set()
    for x, y in dots:
        if axis == 'x' and x > val:
            x = 2 * val - x
        elif axis == 'y' and y > val:
            y = 2 * val - y
        new_dots.add((x, y))

    print(len(new_dots))


if __name__ == "__main__":
    main()
