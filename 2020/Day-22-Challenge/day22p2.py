import os
import sys


def play(p1, p2):
    """Recursive combat. Returns (winner_is_1, deck1, deck2)."""
    seen = set()
    while p1 and p2:
        state = (tuple(p1), tuple(p2))
        if state in seen:
            return True, p1, p2
        seen.add(state)
        a = p1.pop(0)
        b = p2.pop(0)
        if len(p1) >= a and len(p2) >= b:
            sub1, _, _ = play(p1[:a], p2[:b])
            if sub1:
                p1.extend([a, b])
            else:
                p2.extend([b, a])
        else:
            if a > b:
                p1.extend([a, b])
            else:
                p2.extend([b, a])
    return (True, p1, p2) if p1 else (False, p1, p2)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    p1s, p2s = data.split('\n\n')
    p1 = [int(x) for x in p1s.splitlines()[1:] if x.strip()]
    p2 = [int(x) for x in p2s.splitlines()[1:] if x.strip()]

    winner1, deck1, deck2 = play(p1, p2)
    winner = deck1 if winner1 else deck2
    print(sum((i + 1) * c for i, c in enumerate(reversed(winner))))


if __name__ == "__main__":
    main()
