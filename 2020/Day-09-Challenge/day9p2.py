import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        nums = [int(line) for line in f if line.strip()]

    # find the invalid number first (same as part 1)
    preamble = 25
    invalid = None
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
            invalid = target
            break

    # find a contiguous range summing to it
    lo = 0
    hi = 1
    s = nums[lo] + nums[hi]
    while hi < len(nums):
        if s == invalid:
            rng = nums[lo:hi + 1]
            print(min(rng) + max(rng))
            return
        if s < invalid:
            hi += 1
            s += nums[hi]
        else:
            s -= nums[lo]
            lo += 1


if __name__ == "__main__":
    main()
