import os
import sys

SHAPES = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
]


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        jets = f.read().strip()

    W = 7
    occupied = set()
    top = 0
    jet_idx = 0
    n_jet = len(jets)

    def can_place(shape, x, y):
        for dx, dy in shape:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= W or ny < 0:
                return False
            if (nx, ny) in occupied:
                return False
        return True

    # cycle detection: (rock % 5, jet_idx, top profile) -> (rock, top)
    seen = {}
    heights = []
    TARGET = 1000000000000

    rock = 0
    while rock < TARGET:
        shape = SHAPES[rock % 5]
        x, y = 2, top + 3
        while True:
            j = jets[jet_idx % n_jet]
            jet_idx += 1
            dx = 1 if j == '>' else -1
            if can_place(shape, x + dx, y):
                x += dx
            if can_place(shape, x, y - 1):
                y -= 1
            else:
                for dx2, dy2 in shape:
                    occupied.add((x + dx2, y + dy2))
                top = max(top, y + 1 + max(dy2 for dx2, dy2 in shape))
                break
        heights.append(top)

        # profile of top 30 rows
        profile = []
        for yy in range(top - 30, top):
            mask = 0
            for xx in range(W):
                if (xx, yy) in occupied:
                    mask |= 1 << xx
            profile.append(mask)
        key = (rock % 5, jet_idx % n_jet, tuple(profile))
        if key in seen:
            prev_rock, prev_top = seen[key]
            cycle_len = rock - prev_rock
            cycle_height = top - prev_top
            remaining = TARGET - rock
            cycles = remaining // cycle_len
            if cycles > 0:
                rock += cycles * cycle_len
                offset = cycles * cycle_height
                top += offset
                occupied = {(x, y + offset) for x, y in occupied}
                seen.clear()
        else:
            seen[key] = (rock, top)
        rock += 1

    print(top)


if __name__ == "__main__":
    main()
