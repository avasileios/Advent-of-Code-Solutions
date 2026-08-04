import os
import sys


def play(p1, p2):
    while p1 and p2:
        a = p1.pop(0)
        b = p2.pop(0)
        if a > b:
            p1.extend([a, b])
        else:
            p2.extend([b, a])
    winner = p1 if p1 else p2
    return sum((i + 1) * c for i, c in enumerate(reversed(winner)))


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    p1s, p2s = data.split('\n\n')
    p1 = [int(x) for x in p1s.splitlines()[1:] if x.strip()]
    p2 = [int(x) for x in p2s.splitlines()[1:] if x.strip()]

    print(play(p1, p2))


if __name__ == "__main__":
    main()
