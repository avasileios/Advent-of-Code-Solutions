import os
import sys
import re


def apply_mask(value, mask):
    for i, c in enumerate(mask):
        if c == 'X':
            continue
        bit = 35 - i
        if c == '1':
            value |= 1 << bit
        else:
            value &= ~(1 << bit)
    return value


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    mem = {}
    mask = 'X' * 36
    for line in lines:
        if line.startswith('mask'):
            mask = line.split(' = ')[1]
        else:
            m = re.match(r'mem\[(\d+)\] = (\d+)', line)
            addr, value = int(m.group(1)), int(m.group(2))
            mem[addr] = apply_mask(value, mask)

    print(sum(mem.values()))


if __name__ == "__main__":
    main()
