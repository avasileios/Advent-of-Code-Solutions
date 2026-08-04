import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    parts = data.split('\n\n')
    drawn = [int(x) for x in parts[0].split(',')]
    boards = []
    for block in parts[1:]:
        board = []
        for line in block.splitlines():
            if line.strip():
                board.append([int(x) for x in line.split()])
        boards.append(board)

    n = len(boards)
    marked = [[[False] * 5 for _ in range(5)] for _ in range(n)]
    won = [False] * n
    remaining = n

    def check_win(bi):
        for r in range(5):
            if all(marked[bi][r][c] for c in range(5)):
                return True
        for c in range(5):
            if all(marked[bi][r][c] for r in range(5)):
                return True
        return False

    def score(bi, last):
        s = 0
        for r in range(5):
            for c in range(5):
                if not marked[bi][r][c]:
                    s += boards[bi][r][c]
        return s * last

    for num in drawn:
        for bi in range(n):
            if won[bi]:
                continue
            for r in range(5):
                for c in range(5):
                    if boards[bi][r][c] == num:
                        marked[bi][r][c] = True
            if check_win(bi):
                won[bi] = True
                remaining -= 1
                if remaining == 0:
                    print(score(bi, num))
                    return


if __name__ == "__main__":
    main()
