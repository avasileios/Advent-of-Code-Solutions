import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    total = 0
    for line in lines:
        vals = list(map(int, line.split()))
        first_vals = []
        while any(vals):
            first_vals.append(vals[0])
            vals = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
        # extrapolate backwards: result = first - result
        result = 0
        for v in reversed(first_vals):
            result = v - result
        total += result
    print(total)


if __name__ == "__main__":
    main()
