import os
import sys
from collections import defaultdict


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    template = lines[0]
    rules = {}
    for line in lines[1:]:
        a, b = line.split(' -> ')
        rules[a] = b

    pairs = defaultdict(int)
    for i in range(len(template) - 1):
        pairs[template[i:i + 2]] += 1

    for _ in range(40):
        new_pairs = defaultdict(int)
        for pair, count in pairs.items():
            ins = rules[pair]
            new_pairs[pair[0] + ins] += count
            new_pairs[ins + pair[1]] += count
        pairs = new_pairs

    counts = defaultdict(int)
    for (a, b), count in pairs.items():
        counts[a] += count
    counts[template[-1]] += 1

    print(max(counts.values()) - min(counts.values()))


if __name__ == "__main__":
    main()
