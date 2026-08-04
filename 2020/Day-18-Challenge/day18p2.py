import os
import sys


def evaluate(expr, precedence):
    tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
    pos = 0

    def parse(level):
        nonlocal pos
        if level == len(precedence):
            t = tokens[pos]
            if t == '(':
                pos += 1
                val = parse(0)
                pos += 1  # skip ')'
                return val
            pos += 1
            return int(t)
        val = parse(level + 1)
        while pos < len(tokens) and tokens[pos] in precedence[level]:
            op = tokens[pos]
            pos += 1
            rhs = parse(level + 1)
            if op == '+':
                val += rhs
            else:
                val *= rhs
        return val

    return parse(0)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total = 0
    for line in lines:
        total += evaluate(line, [('*',), ('+',)])

    print(total)


if __name__ == "__main__":
    main()
