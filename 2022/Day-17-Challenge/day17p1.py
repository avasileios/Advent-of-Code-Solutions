import os
import sys

SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],          # -
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],  # +
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # L (reversed)
    [(0, 0), (0, 1), (0, 2), (0, 3)],          # |
    [(0, 0), (1, 0), (0, 1), (1, 1)],          # o
]


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        jets = f.read().strip()

    W = 7
    occupied = set()
    top = 0  # highest y + 1
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

    for rock in range(2022):
        shape = SHAPES[rock % 5]
        x, y = 2, top + 3
        while True:
            # jet push
            j = jets[jet_idx % n_jet]
            jet_idx += 1
            dx = 1 if j == '>' else -1
            if can_place(shape, x + dx, y):
                x += dx
            # fall
            if can_place(shape, x, y - 1):
                y -= 1
            else:
                for dx2, dy2 in shape:
                    occupied.add((x + dx2, y + dy2))
                    top = max(top, y + dy2 + 1)
                break

    print(top)


if __name__ == "__main__":
    main()
