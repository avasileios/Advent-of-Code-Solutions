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

    n = len(hails)
    maxv = max(max(abs(h[3]), abs(h[4])) for h in hails)

    # brute force rock velocity (vx, vy). For rock start (px, py) and
    # hailstone i:  px + vx*ti = hx + hvx*ti  ->  (hx - px) = (vx - hvx) * ti
    # so every hailstone's relative position must be parallel to its relative
    # velocity: (hx - px, hy - py) = ti * (vx - hvx, vy - hvy).
    # For two hailstones 0 and 1, solve for t0, t1, px, py:
    # p0 + (v0 - v) t0 = p1 + (v1 - v) t1
    def solve_t01(vx, vy):
        p0x, p0y, _, v0x, v0y, _ = hails[0]
        p1x, p1y, _, v1x, v1y, _ = hails[1]
        a11 = v0x - vx
        a12 = -(v1x - vx)
        a21 = v0y - vy
        a22 = -(v1y - vy)
        b1 = p1x - p0x
        b2 = p1y - p0y
        det = a11 * a22 - a12 * a21
        if det == 0:
            return None
        t0 = (b1 * a22 - a12 * b2) / det
        t1 = (a11 * b2 - b1 * a21) / det
        if t0 <= 0 or t1 <= 0:
            return None
        px = p0x + (v0x - vx) * t0
        py = p0y + (v0y - vy) * t0
        return t0, t1, px, py

    for vx in range(-maxv - 10, maxv + 11):
        for vy in range(-maxv - 10, maxv + 11):
            r = solve_t01(vx, vy)
            if r is None:
                continue
            t0, t1, px, py = r
            # fast filter with hailstone 2: relative pos parallel to rel vel
            h2 = hails[2]
            ok = True
            for hx, hy, hz, hvx, hvy, hvz in (hails[0], hails[1], hails[2]):
                rvx, rvy = vx - hvx, vy - hvy
                dx, dy = hx - px, hy - py
                if dx * rvy != dy * rvx:
                    ok = False
                    break
            if not ok:
                continue
            # verify all hailstones in xy
            ok = True
            for hx, hy, hz, hvx, hvy, hvz in hails:
                rvx, rvy = vx - hvx, vy - hvy
                dx, dy = hx - px, hy - py
                if dx * rvy != dy * rvx:
                    ok = False
                    break
            if not ok:
                continue
            # find vz: pz + vz*ti = hz + hvz*ti for all i
            # from hailstones 0 and 1: pz = h0z + (h0vz - vz) t0 = h1z + (h1vz - vz) t1
            h0, h1 = hails[0], hails[1]
            num = h0[2] - h1[2] + h0[5] * t0 - h1[5] * t1
            if abs(t0 - t1) < 1e-9:
                continue
            vz = num / (t0 - t1)
            if abs(vz - round(vz)) > 1e-6:
                continue
            vz = round(vz)
            pz = h0[2] + (h0[5] - vz) * t0
            # verify z for all
            okz = True
            for hx, hy, hz, hvx, hvy, hvz in hails:
                rvx, rvy = vx - hvx, vy - hvy
                if rvx == 0 and rvy == 0:
                    ti = 0
                elif rvx != 0:
                    ti = (hx - px) / rvx
                else:
                    ti = (hy - py) / rvy
                if abs((hz + hvz * ti) - (pz + vz * ti)) > 1e-3:
                    okz = False
                    break
            if okz:
                print(round(px) + round(py) + round(pz))
                return


if __name__ == "__main__":
    main()
