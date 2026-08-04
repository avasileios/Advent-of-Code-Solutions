import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    blocks = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('inp'):
            div = int(lines[i + 4].split()[-1])
            x_off = int(lines[i + 5].split()[-1])
            y_off = int(lines[i + 15].split()[-1])
            blocks.append((div, x_off, y_off))
            i += 18
        else:
            i += 1

    pairs = []
    stack = []
    for idx, (div, x_off, y_off) in enumerate(blocks):
        if div == 1:
            stack.append((idx, y_off))
        else:
            push_idx, y_push = stack.pop()
            pairs.append((push_idx, idx, y_push + x_off))

    digits = [0] * 14
    for push_idx, pop_idx, delta in pairs:
        # minimize
        if delta >= 0:
            digits[push_idx] = 1
            digits[pop_idx] = 1 + delta
        else:
            digits[push_idx] = 1 - delta
            digits[pop_idx] = 1

    print(''.join(str(d) for d in digits))


if __name__ == "__main__":
    main()
