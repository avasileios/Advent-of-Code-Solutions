import os
import sys


def repunit_geometric(d, m):
    """Sum_{i=0}^{m-1} 10^(d*i)"""
    return (10 ** (d * m) - 1) // (10 ** d - 1)


def sum_range(lo, hi):
    """Sum of all integers k in [lo, hi]"""
    if lo > hi:
        return 0
    return (lo + hi) * (hi - lo + 1) // 2


def primitive_sum(d, lo, hi):
    """Sum of all d-digit numbers k in [lo, hi] that are NOT a repetition
    of a shorter block (i.e. whose minimal period is d)."""
    lo = max(lo, 10 ** (d - 1))
    hi = min(hi, 10 ** d - 1)
    if lo > hi:
        return 0
    total = sum_range(lo, hi)
    # subtract numbers that are a repetition of a block with period p | d
    for p in range(1, d):
        if d % p != 0:
            continue
        j = d // p
        if j < 2:
            continue
        r = repunit_geometric(p, j)  # k = block * r
        block_lo = (lo + r - 1) // r
        block_hi = hi // r
        total -= r * primitive_sum(p, block_lo, block_hi)
    return total


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        text = f.read().strip()

    ranges = []
    for tok in text.split(','):
        a, b = tok.split('-')
        ranges.append((int(a), int(b)))

    max_digits = max(len(str(b)) for _, b in ranges)

    total = 0
    for a, b in ranges:
        # invalid IDs: block of d digits repeated m >= 2 times -> total
        # length m*d. The number is k * repunit_geometric(d, m).
        for d in range(1, max_digits + 1):
            for m in range(2, max_digits // d + 1):
                r = repunit_geometric(d, m)
                klo = (a + r - 1) // r
                khi = b // r
                if klo > khi:
                    continue
                total += r * primitive_sum(d, klo, khi)

    print(total)


if __name__ == "__main__":
    main()
