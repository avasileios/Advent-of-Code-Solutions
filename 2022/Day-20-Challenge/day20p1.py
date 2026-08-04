import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        nums = [int(l.strip()) for l in f if l.strip()]

    n = len(nums)
    # store (original_index, value) to handle duplicates
    items = list(enumerate(nums))
    for i in range(n):
        pos = next(j for j, (oi, v) in enumerate(items) if oi == i)
        _, v = items[pos]
        del items[pos]
        new_pos = (pos + v) % (n - 1)
        items.insert(new_pos, (i, v))

    vals = [v for _, v in items]
    zi = vals.index(0)
    a = vals[(zi + 1000) % n]
    b = vals[(zi + 2000) % n]
    c = vals[(zi + 3000) % n]
    print(a + b + c)


if __name__ == "__main__":
    main()
