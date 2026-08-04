import os
import sys


def phase_digit(digits, pos):
    """Output digit for position pos after one FFT phase."""
    base = [0, 1, 0, -1]
    total = 0
    for i, d in enumerate(digits):
        pattern_idx = ((i + 1) // (pos + 1)) % 4
        total += d * base[pattern_idx]
    return abs(total) % 10


def phase(signal):
    return [phase_digit(signal, i) for i in range(len(signal))]


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        signal = [int(c) for c in f.read().strip()]

    for _ in range(100):
        signal = phase(signal)

    print(''.join(str(d) for d in signal[:8]))


if __name__ == "__main__":
    main()
