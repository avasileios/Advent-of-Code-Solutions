import os
import sys
import re
from itertools import combinations


def parse_machine(line):
    # e.g. [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    target_part = line.split(']')[0] + ']'
    target = target_part.strip('[]')
    target_mask = 0
    for i, ch in enumerate(target):
        if ch == '#':
            target_mask |= 1 << i

    buttons = []
    for m in re.finditer(r'\(([^)]*)\)', line):
        indices = [int(x) for x in m.group(1).split(',') if x.strip()]
        mask = 0
        for idx in indices:
            mask |= 1 << idx
        buttons.append(mask)

    return target_mask, buttons


def min_presses(target_mask, buttons):
    b = len(buttons)
    # Try subsets by increasing size (pressing a button twice cancels out)
    for k in range(0, b + 1):
        for combo in combinations(range(b), k):
            xor_sum = 0
            for idx in combo:
                xor_sum ^= buttons[idx]
            if xor_sum == target_mask:
                return k
    return None


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total = 0
    for line in lines:
        target, buttons = parse_machine(line)
        total += min_presses(target, buttons)

    print(total)


if __name__ == "__main__":
    main()
