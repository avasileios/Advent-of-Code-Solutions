import os
import sys


def score(line):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{', '>': '<'}
    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    for c in line:
        if c in '([{<':
            stack.append(c)
        else:
            if not stack or stack[-1] != pairs[c]:
                return scores[c]
            stack.pop()
    return 0


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    print(sum(score(line) for line in lines))


if __name__ == "__main__":
    main()
