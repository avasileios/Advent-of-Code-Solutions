import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    total = 0
    for line in lines:
        _, rest = line.split(': ')
        red = green = blue = 0
        for subset in rest.split('; '):
            for count, color in re.findall(r'(\d+) (\w+)', subset):
                count = int(count)
                if color == 'red':
                    red = max(red, count)
                if color == 'green':
                    green = max(green, count)
                if color == 'blue':
                    blue = max(blue, count)
        total += red * green * blue
    print(total)


if __name__ == "__main__":
    main()
