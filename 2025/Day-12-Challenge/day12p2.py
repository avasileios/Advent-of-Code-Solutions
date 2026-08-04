import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    # Part 2 of Day 12 is a free star: no computation is needed.
    print("merry christmas")


if __name__ == "__main__":
    main()
