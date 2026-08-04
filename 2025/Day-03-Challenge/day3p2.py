import os
import sys


def largest_subsequence(digits, keep):
    """Largest subsequence of `digits` (keeping order) of length `keep`."""
    stack = []
    to_remove = len(digits) - keep
    for ch in digits:
        while to_remove > 0 and stack and stack[-1] < ch:
            stack.pop()
            to_remove -= 1
        stack.append(ch)
    return int("".join(stack[:keep]))


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        banks = [line.strip() for line in f if line.strip()]

    total = 0
    for bank in banks:
        total += largest_subsequence(bank, 12)

    print(total)


if __name__ == "__main__":
    main()
