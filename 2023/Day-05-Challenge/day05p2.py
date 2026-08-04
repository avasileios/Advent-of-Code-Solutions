import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    seed_ranges = list(map(int, lines[0].split(': ')[1].split()))
    ranges = []
    for i in range(0, len(seed_ranges), 2):
        ranges.append((seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1] - 1))

    maps = []
    current = []
    for line in lines[2:]:
        if 'map' in line:
            if current:
                maps.append(current)
            current = []
        else:
            current.append(tuple(map(int, line.split())))
    maps.append(current)

    # apply a map to a list of ranges: returns list of ranges (possibly split)
    def apply_map(ranges, m):
        result = []
        for lo, hi in ranges:
            remaining = [(lo, hi)]
            for dst, src, rng in m:
                src_hi = src + rng - 1
                new_remaining = []
                for rlo, rhi in remaining:
                    # overlap?
                    if rhi < src or rlo > src_hi:
                        new_remaining.append((rlo, rhi))
                        continue
                    # left part
                    if rlo < src:
                        new_remaining.append((rlo, src - 1))
                    # middle (mapped)
                    mid_lo = max(rlo, src)
                    mid_hi = min(rhi, src_hi)
                    result.append((dst + (mid_lo - src), dst + (mid_hi - src)))
                    # right part
                    if rhi > src_hi:
                        new_remaining.append((src_hi + 1, rhi))
                remaining = new_remaining
            result.extend(remaining)
        return result

    for m in maps:
        ranges = apply_map(ranges, m)

    print(min(lo for lo, hi in ranges))


if __name__ == "__main__":
    main()
