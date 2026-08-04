import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    hails = []
    for line in lines:
        nums = list(map(int, re.findall(r'-?\d+', line)))
        hails.append((nums[0], nums[1], nums[2], nums[3], nums[4], nums[5]))

    # test area
    lo, hi = 200000000000000, 400000000000000
    total = 0
    for i in range(len(hails)):
        x1, y1, _, vx1, vy1, _ = hails[i]
        for j in range(i + 1, len(hails)):
            x2, y2, _, vx2, vy2, _ = hails[j]
            # line intersection (2D, t >= 0)
            det = vx1 * vy2 - vx2 * vy1
            if det == 0:
                continue
            # p1 + v1 t1 = p2 + v2 t2
            dx = x2 - x1
            dy = y2 - y1
            t1 = (dx * vy2 - dy * vx2) / det
            t2 = (dx * vy1 - dy * vx1) / det
            if t1 < 0 or t2 < 0:
                continue
            ix = x1 + vx1 * t1
            iy = y1 + vy1 * t1
            if lo <= ix <= hi and lo <= iy <= hi:
                total += 1
    print(total)


if __name__ == "__main__":
    main()
