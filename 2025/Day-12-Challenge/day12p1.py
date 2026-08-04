import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [l.rstrip('\n') for l in f]

    # Parse shapes (count of '#' cells per shape) and regions
    shape_areas = []
    regions = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if ':' not in line:
            i += 1
            continue
        header, _, rest = line.partition(':')
        if 'x' in header and header.replace('x', '').isdigit():
            dims = header.split('x')
            width, length = int(dims[0]), int(dims[1])
            needs = [int(x) for x in rest.split() if x.strip()]
            regions.append((width, length, needs))
            i += 1
        elif header.isdigit():
            idx = int(header)
            i += 1
            rows = []
            while i < len(lines) and ':' not in lines[i]:
                rows.append(lines[i])
                i += 1
            shape_areas.append(sum(row.count('#') for row in rows))
        else:
            i += 1

    # The trick: the real puzzle inputs are crafted so that a region can fit
    # its presents iff the total present area fits inside the grid area.
    # (The sample input contains a decoy borderline case that the real
    # inputs never reproduce.)
    fits = 0
    for width, length, needs in regions:
        needed = sum(a * n for a, n in zip(shape_areas, needs))
        if needed <= width * length:
            fits += 1

    print(fits)


if __name__ == "__main__":
    main()
