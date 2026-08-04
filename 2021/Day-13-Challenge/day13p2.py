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

    for axis, val in folds:
        new_dots = set()
        for x, y in dots:
            if axis == 'x' and x > val:
                x = 2 * val - x
            elif axis == 'y' and y > val:
                y = 2 * val - y
            new_dots.add((x, y))
        dots = new_dots

    # print the code
    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)
    for y in range(max_y + 1):
        print(''.join('#' if (x, y) in dots else ' ' for x in range(max_x + 1)))


if __name__ == "__main__":
    main()
