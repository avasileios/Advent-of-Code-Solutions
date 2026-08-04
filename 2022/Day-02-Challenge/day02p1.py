import os
import sys


def score(them, me):
    # A/X rock, B/Y paper, C/Z scissors
    v = {'X': 1, 'Y': 2, 'Z': 3}[me]
    win = {(('A', 'Y')), (('B', 'Z')), (('C', 'X'))}
    draw = {(('A', 'X')), (('B', 'Y')), (('C', 'Z'))}
    if (them, me) in win:
        return v + 6
    if (them, me) in draw:
        return v + 3
    return v


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    total = 0
    for line in lines:
        them, me = line.split()
        total += score(them, me)
    print(total)


if __name__ == "__main__":
    main()
