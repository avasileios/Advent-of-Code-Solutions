import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    rows = [line.split() for line in lines]
    operators = rows[-1]
    number_rows = rows[:-1]

    grand_total = 0
    for col in range(len(operators)):
        op = operators[col]
        values = [int(number_rows[r][col]) for r in range(len(number_rows))]
        if op == '+':
            grand_total += sum(values)
        else:
            product = 1
            for v in values:
                product *= v
            grand_total += product

    print(grand_total)


if __name__ == "__main__":
    main()
