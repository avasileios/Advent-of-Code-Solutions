import os
import sys

S2D = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}


def snafu_to_dec(s):
    total = 0
    for c in s:
        total = total * 5 + S2D[c]
    return total


def dec_to_snafu(n):
    if n == 0:
        return '0'
    digits = []
    while n:
        r = n % 5
        if r <= 2:
            digits.append(str(r))
            n //= 5
        else:
            digits.append('=' if r == 3 else '-')
            n = n // 5 + 1
    return ''.join(reversed(digits))


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    total = sum(snafu_to_dec(l) for l in lines)
    print(dec_to_snafu(total))


if __name__ == "__main__":
    main()
