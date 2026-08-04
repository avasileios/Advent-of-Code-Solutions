import os
import sys
import re


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    foods = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r'(.+) \(contains (.+)\)', line)
            ingredients = set(m.group(1).split())
            allergens = set(m.group(2).split(', '))
            foods.append((ingredients, allergens))

    candidates = {}
    for ingredients, allergens in foods:
        for a in allergens:
            if a in candidates:
                candidates[a] &= ingredients
            else:
                candidates[a] = set(ingredients)

    # deduce: assign the unique ingredient to each allergen
    assigned = {}
    while candidates:
        for a in list(candidates):
            remaining = candidates[a] - set(assigned.values())
            if len(remaining) == 1:
                assigned[a] = remaining.pop()
                del candidates[a]

    dangerous = ','.join(assigned[a] for a in sorted(assigned))
    print(dangerous)


if __name__ == "__main__":
    main()
