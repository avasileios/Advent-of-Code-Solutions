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
        game, rest = line.split(': ')
        gid = int(game.split()[1])
        possible = True
        for subset in rest.split('; '):
            for count, color in re.findall(r'(\d+) (\w+)', subset):
                count = int(count)
                if color == 'red' and count > 12:
                    possible = False
                if color == 'green' and count > 13:
                    possible = False
                if color == 'blue' and count > 14:
                    possible = False
        if possible:
            total += gid
    print(total)


if __name__ == "__main__":
    main()
