import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    exprs = {}
    for line in lines:
        name, rest = line.split(': ')
        exprs[name] = rest

    def evaluate(name):
        e = exprs[name]
        parts = e.split()
        if len(parts) == 1:
            return int(parts[0])
        a, op, b = parts
        va, vb = evaluate(a), evaluate(b)
        return {'+': va + vb, '-': va - vb, '*': va * vb, '/': va // vb}[op]

    print(evaluate('root'))


if __name__ == "__main__":
    main()
