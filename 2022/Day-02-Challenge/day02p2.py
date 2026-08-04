import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    total = 0
    for line in lines:
        them, outcome = line.split()
        # X lose, Y draw, Z win
        beats = {'A': 'B', 'B': 'C', 'C': 'A'}
        loses = {'A': 'C', 'B': 'A', 'C': 'B'}
        if outcome == 'X':
            me = loses[them]
            total += 0
        elif outcome == 'Y':
            me = them
            total += 3
        else:
            me = beats[them]
            total += 6
        total += {'A': 1, 'B': 2, 'C': 3}[me]
    print(total)


if __name__ == "__main__":
    main()
