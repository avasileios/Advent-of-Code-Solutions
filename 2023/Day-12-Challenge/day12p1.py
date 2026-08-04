import os
import sys
from functools import lru_cache


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    total = 0
    for line in lines:
        springs, groups = line.split()
        groups = tuple(map(int, groups.split(',')))

        @lru_cache(maxsize=None)
        def count(pos, gi, current):
            # pos: position in springs; gi: current group index; current: size of current run
            if pos == len(springs):
                if gi == len(groups) and current == 0:
                    return 1
                if gi == len(groups) - 1 and current == groups[gi]:
                    return 1
                return 0
            total_c = 0
            for ch in ('.', '#'):
                if springs[pos] != '?' and springs[pos] != ch:
                    continue
                if ch == '#':
                    total_c += count(pos + 1, gi, current + 1)
                else:
                    if current > 0:
                        if gi < len(groups) and current == groups[gi]:
                            total_c += count(pos + 1, gi + 1, 0)
                    else:
                        total_c += count(pos + 1, gi, 0)
            return total_c

        total += count(0, 0, 0)
    print(total)


if __name__ == "__main__":
    main()
