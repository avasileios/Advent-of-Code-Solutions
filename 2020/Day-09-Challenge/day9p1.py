import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        nums = [int(line) for line in f if line.strip()]

    preamble = 25
    for i in range(preamble, len(nums)):
        window = nums[i - preamble:i]
        target = nums[i]
        found = False
        for a in range(len(window)):
            for b in range(a + 1, len(window)):
                if window[a] + window[b] == target:
                    found = True
                    break
            if found:
                break
        if not found:
            print(target)
            return


if __name__ == "__main__":
    main()
