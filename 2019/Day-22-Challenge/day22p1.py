import os
import sys


def apply(deck, line):
    parts = line.split()
    if line.startswith('deal into new stack'):
        deck.reverse()
    elif line.startswith('cut'):
        k = int(parts[-1])
        deck = deck[k:] + deck[:k]
    elif line.startswith('deal with increment'):
        k = int(parts[-1])
        n = len(deck)
        new = [0] * n
        for i, c in enumerate(deck):
            new[(i * k) % n] = c
        deck = new
    return deck


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    deck = list(range(10007))
    for line in lines:
        deck = apply(deck, line)

    print(deck.index(2019))


if __name__ == "__main__":
    main()
