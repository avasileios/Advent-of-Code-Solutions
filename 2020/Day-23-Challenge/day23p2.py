import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        start = [int(c) for c in f.read().strip()]

    n = 1000000
    # circular linked list: nxt[c] = the cup after cup c
    nxt = {}
    cups = start + list(range(max(start) + 1, n + 1))
    for i in range(n - 1):
        nxt[cups[i]] = cups[i + 1]
    nxt[cups[-1]] = cups[0]

    cur = cups[0]
    for _ in range(10000000):
        a = nxt[cur]
        b = nxt[a]
        c = nxt[b]
        # destination
        dest = cur - 1
        while dest < 1 or dest in (a, b, c):
            dest -= 1
            if dest < 1:
                dest = n
        nxt[cur] = nxt[c]
        nxt[c] = nxt[dest]
        nxt[dest] = a
        cur = nxt[cur]

    a = nxt[1]
    b = nxt[a]
    print(a * b)


if __name__ == "__main__":
    main()
