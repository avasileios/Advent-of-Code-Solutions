import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    total = 0
    for group in data.split('\n\n'):
        answers = set()
        for person in group.split():
            answers.update(person)
        total += len(answers)

    print(total)


if __name__ == "__main__":
    main()
