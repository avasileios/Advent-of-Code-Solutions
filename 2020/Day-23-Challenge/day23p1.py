import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        cups = [int(c) for c in f.read().strip()]

    n = len(cups)
    cur = cups[0]
    for _ in range(100):
        cur_idx = cups.index(cur)
        picked = [cups[(cur_idx + 1 + i) % n] for i in range(3)]
        for c in picked:
            cups.remove(c)
        dest = cur - 1
        while dest not in cups:
            dest -= 1
            if dest < 1:
                dest = max(cups)
        di = cups.index(dest)
        cups[di + 1:di + 1] = picked
        cur = cups[(cups.index(cur) + 1) % n]

    idx1 = cups.index(1)
    result = ''.join(str(c) for c in cups[idx1 + 1:] + cups[:idx1])
    print(result)


if __name__ == "__main__":
    main()
