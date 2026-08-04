import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read().strip()
    for i in range(14, len(data) + 1):
        if len(set(data[i - 14:i])) == 14:
            print(i)
            return


if __name__ == "__main__":
    main()
