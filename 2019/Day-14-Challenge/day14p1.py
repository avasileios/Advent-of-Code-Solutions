import os
import sys
import math


def parse_reactions(lines):
    reactions = {}  # product -> (amount, [(qty, chem), ...])
    for line in lines:
        left, _, right = line.strip().partition(' => ')
        qty, chem = right.split(' ')
        inputs = []
        for part in left.split(', '):
            q, c = part.split(' ')
            inputs.append((int(q), c))
        reactions[chem] = (int(qty), inputs)
    return reactions


def ore_needed(reactions, fuel_amount):
    need = {'FUEL': fuel_amount}
    surplus = {}
    ore = 0
    while need:
        chem, qty = need.popitem()
        if chem == 'ORE':
            ore += qty
            continue
        have = surplus.get(chem, 0)
        if have >= qty:
            surplus[chem] = have - qty
            continue
        qty -= have
        surplus[chem] = 0
        amount, inputs = reactions[chem]
        batches = math.ceil(qty / amount)
        produced = batches * amount
        surplus[chem] = produced - qty
        for q, c in inputs:
            need[c] = need.get(c, 0) + q * batches
    return ore


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        reactions = parse_reactions([line for line in f if line.strip()])

    print(ore_needed(reactions, 1))


if __name__ == "__main__":
    main()
