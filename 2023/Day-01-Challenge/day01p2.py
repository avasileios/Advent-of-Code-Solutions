import os
import sys

WORDS = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
         'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    total = 0
    for line in lines:
        # find all digit/word matches left to right
        found = []
        for i in range(len(line)):
            if line[i].isdigit():
                found.append(line[i])
            else:
                for w, d in WORDS.items():
                    if line.startswith(w, i):
                        found.append(d)
                        break
        total += int(found[0] + found[-1])
    print(total)


if __name__ == "__main__":
    main()
