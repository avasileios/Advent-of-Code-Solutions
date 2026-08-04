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

    packets = []
    for p in data.strip().split('\n\n'):
        for line in p.splitlines():
            packets.append(json.loads(line))
    packets.append([[2]])
    packets.append([[6]])

    from functools import cmp_to_key
    packets.sort(key=cmp_to_key(cmp))

    i2 = packets.index([[2]]) + 1
    i6 = packets.index([[6]]) + 1
    print(i2 * i6)


if __name__ == "__main__":
    main()
