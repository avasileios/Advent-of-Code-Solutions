import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read().strip()

    signal = [int(c) for c in data] * 10000
    offset = int(data[:7])

    # The offset is more than half the signal, so every output digit in the
    # interesting region is just the cumulative sum (mod 10) of the digits
    # from itself to the end.  Repeat 100 times.
    digits = signal[offset:]
    for _ in range(100):
        s = 0
        for i in range(len(digits) - 1, -1, -1):
            s += digits[i]
            digits[i] = s % 10

    print(''.join(str(d) for d in digits[:8]))


if __name__ == "__main__":
    main()
