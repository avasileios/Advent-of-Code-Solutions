import os
import sys
import bisect
from collections import defaultdict


def merge_intervals(intervals):
    """Merge inclusive integer intervals [(a, b), ...]."""
    if not intervals:
        return []
    intervals.sort()
    merged = []
    cur_a, cur_b = intervals[0]
    for a, b in intervals[1:]:
        if a <= cur_b + 1:
            cur_b = max(cur_b, b)
        else:
            merged.append((cur_a, cur_b))
            cur_a, cur_b = a, b
    merged.append((cur_a, cur_b))
    return merged


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        reds = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split(','))
            reds.append((x, y))

    n = len(reds)
    # loop segments between consecutive red tiles (the list wraps around)
    h_segs = []  # (y, xa, xb)
    v_segs = []  # (x, ya, yb)
    for i in range(n):
        x1, y1 = reds[i]
        x2, y2 = reds[(i + 1) % n]
        if y1 == y2:
            h_segs.append((y1, min(x1, x2), max(x1, x2)))
        else:
            v_segs.append((x1, min(y1, y2), max(y1, y2)))

    h_by_y = defaultdict(list)
    for y, xa, xb in h_segs:
        h_by_y[y].append((xa, xb))
    v_by_x = defaultdict(list)
    for x, ya, yb in v_segs:
        v_by_x[x].append((ya, yb))

    # For each row y that contains a red tile: the "filled" spans at that row
    # = loop cells (horizontal runs + vertical crossings) plus the even-odd
    # interior between crossings. A rectangle is fully valid iff its four
    # edges lie inside the filled region (the loop is a simple closed curve,
    # so its filled interior is simply connected).
    row_filled = {}
    for y in sorted(set(y for _, y in reds)):
        # half-open crossings (standard even-odd rule): a vertical segment
        # crosses the row only when ya <= y < yb
        crossings = sorted(x for x, ya, yb in v_segs if ya <= y < yb)
        intervals = []
        for k in range(0, len(crossings) - 1, 2):
            intervals.append((crossings[k], crossings[k + 1]))
        intervals.extend(h_by_y.get(y, []))
        row_filled[y] = merge_intervals(intervals)

    col_filled = {}
    for x in sorted(set(x for x, _ in reds)):
        crossings = sorted(y for y, xa, xb in h_segs if xa <= x < xb)
        intervals = []
        for k in range(0, len(crossings) - 1, 2):
            intervals.append((crossings[k], crossings[k + 1]))
        intervals.extend(v_by_x.get(x, []))
        col_filled[x] = merge_intervals(intervals)

    def edge_covered(intervals, lo, hi):
        """Is the inclusive segment [lo, hi] covered by the merged intervals?"""
        starts = [a for a, b in intervals]
        idx = bisect.bisect_right(starts, lo) - 1
        if idx < 0:
            return False
        a, b = intervals[idx]
        return b >= hi

    red_list = sorted(reds)
    best = 0
    for i in range(len(red_list)):
        x0, y0 = red_list[i]
        for j in range(i + 1, len(red_list)):
            x1, y1 = red_list[j]
            lo_x, hi_x = min(x0, x1), max(x0, x1)
            lo_y, hi_y = min(y0, y1), max(y0, y1)
            if (edge_covered(row_filled[lo_y], lo_x, hi_x) and
                    edge_covered(row_filled[hi_y], lo_x, hi_x) and
                    edge_covered(col_filled[lo_x], lo_y, hi_y) and
                    edge_covered(col_filled[hi_x], lo_y, hi_y)):
                area = (hi_x - lo_x + 1) * (hi_y - lo_y + 1)
                if area > best:
                    best = area

    print(best)


if __name__ == "__main__":
    main()
