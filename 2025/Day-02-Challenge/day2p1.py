import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        text = f.read().strip()

    # Parse ranges: comma separated, each "first-last"
    ranges = []
    for token in text.split(','):
        a, b = token.split('-')
        ranges.append((int(a), int(b)))

    total = 0
    for a, b in ranges:
        # Invalid IDs have the form k*10^d + k, where k has exactly d digits
        # (i.e. the decimal representation of k is repeated twice).
        for d in range(1, 20):
            base = 10 ** d + 1
            lo = (a + base - 1) // base
            hi = b // base
            kmin = max(lo, 10 ** (d - 1))
            kmax = min(hi, 10 ** d - 1)
            if kmin > kmax:
                continue
            n = kmax - kmin + 1
            sum_k = n * (kmin + kmax) // 2
            total += sum_k * base

    print(total)


if __name__ == "__main__":
    main()
