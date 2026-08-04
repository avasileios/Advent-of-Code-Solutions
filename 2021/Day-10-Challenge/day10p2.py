import os
import sys


def completion(line):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{', '>': '<'}
    for c in line:
        if c in '([{<':
            stack.append(c)
        else:
            if not stack or stack[-1] != pairs[c]:
                return None  # corrupted
            stack.pop()
    # incomplete: complete it
    close = { '(': ')', '[': ']', '{': '}', '<': '>' }
    scores = {')': 1, ']': 2, '}': 3, '>': 4}
    total = 0
    for c in reversed(stack):
        total = total * 5 + scores[close[c]]
    return total


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    scores = sorted(s for s in (completion(l) for l in lines) if s is not None)
    print(scores[len(scores) // 2])


if __name__ == "__main__":
    main()
