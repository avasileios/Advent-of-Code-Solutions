import os
import sys
from functools import lru_cache


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    p1 = int(lines[0].split(': ')[1])
    p2 = int(lines[1].split(': ')[1])

    # outcomes of three dice rolls: sum -> multiplicity
    outcomes = {}
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                s = a + b + c
                outcomes[s] = outcomes.get(s, 0) + 1

    @lru_cache(maxsize=None)
    def wins(pos1, score1, pos2, score2):
        """Returns (wins1, wins2) from this state, player 1 to move."""
        w1 = w2 = 0
        for move, mult in outcomes.items():
            np1 = (pos1 - 1 + move) % 10 + 1
            ns1 = score1 + np1
            if ns1 >= 21:
                w1 += mult
            else:
                a, b = wins(pos2, score2, np1, ns1)
                w2 += a * mult
                w1 += b * mult
        return w1, w2

    w1, w2 = wins(p1, 0, p2, 0)
    print(max(w1, w2))


if __name__ == "__main__":
    main()
