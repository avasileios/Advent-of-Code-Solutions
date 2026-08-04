import os
import sys
import json


def cmp(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return (a > b) - (a < b)
    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]
    for x, y in zip(a, b):
        r = cmp(x, y)
        if r:
            return r
    return (len(a) > len(b)) - (len(a) < len(b))


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()

    pairs = [p.splitlines() for p in data.strip().split('\n\n')]
    total = 0
    for i, (a, b) in enumerate(pairs, 1):
        if cmp(json.loads(a), json.loads(b)) < 0:
            total += i
    print(total)


if __name__ == "__main__":
    main()
