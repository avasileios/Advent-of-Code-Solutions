import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    # bag -> list of (count, color)
    rules = {}
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            bag, rest = line.split(' bags contain ')
            rules[bag] = []
            if rest == 'no other bags.':
                continue
            for item in rest.split(', '):
                parts = item.split(' ')
                count = int(parts[0])
                color = ' '.join(parts[1:-1])
                rules[bag].append((count, color))

    def contains_shiny(bag):
        for _, color in rules[bag]:
            if color == 'shiny gold' or contains_shiny(color):
                return True
        return False

    total = sum(1 for bag in rules if contains_shiny(bag))
    print(total)


if __name__ == "__main__":
    main()
