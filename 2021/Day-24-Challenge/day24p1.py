import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # extract the (div, x_off, y_off) triple per digit block
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

    # stack-based pairing: every div=26 block pops the last div=1 block.
    # constraint: w_pop == w_push + (y_push + x_pop)
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
        # w[pop] = w[push] + delta, both in 1..9; maximize
        if delta >= 0:
            digits[push_idx] = 9 - delta
            digits[pop_idx] = 9
        else:
            digits[push_idx] = 9
            digits[pop_idx] = 9 + delta

    print(''.join(str(d) for d in digits))


if __name__ == "__main__":
    main()
