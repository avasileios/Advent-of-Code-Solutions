import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        # raw lines (keep trailing spaces): the alignment matters
        data = [line.rstrip('\n') for line in f]

    # Cephalopod math is written right-to-left in columns: rotate the
    # worksheet 90 degrees counter-clockwise and read each resulting line
    # as a number (the last character is the operator when non-space).
    rotated = zip(*[line[::-1] for line in data])

    total = 0
    problem = []
    for line in rotated:
        if all(ch == ' ' for ch in line):
            continue
        problem.append(int(''.join(line[:-1])))
        if line[-1] != ' ':
            if line[-1] == '+':
                total += sum(problem)
            else:
                prod = 1
                for x in problem:
                    prod *= x
                total += prod
            problem = []

    print(total)


if __name__ == "__main__":
    main()
