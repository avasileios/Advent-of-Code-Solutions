import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    p1 = int(lines[0].split(': ')[1])
    p2 = int(lines[1].split(': ')[1])

    pos1, pos2 = p1, p2
    score1 = score2 = 0
    die = 0
    rolls = 0

    while True:
        # player 1
        move = 0
        for _ in range(3):
            die = die % 100 + 1
            rolls += 1
            move += die
        pos1 = (pos1 - 1 + move) % 10 + 1
        score1 += pos1
        if score1 >= 1000:
            print(score2 * rolls)
            return
        # player 2
        move = 0
        for _ in range(3):
            die = die % 100 + 1
            rolls += 1
            move += die
        pos2 = (pos2 - 1 + move) % 10 + 1
        score2 += pos2
        if score2 >= 1000:
            print(score1 * rolls)
            return


if __name__ == "__main__":
    main()
