import os
import string

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def react_polymer(polymer):
    stack = []
    for unit in polymer:
        if stack:
            # Check for opposite polarity (aA or Aa)
            if abs(ord(unit) - ord(stack[-1])) == 32:
                stack.pop()
                continue
        stack.append(unit)
    return len(stack)

def find_best_reduction(path):
    with open(path, 'r') as f:
        original_polymer = f.read().strip()

    # Get all unique unit types (a through z)
    unit_types = set(original_polymer.lower())
    
    results = {}

    for unit in unit_types:
        # Remove both polarities of the chosen unit
        # (e.g., if unit is 'a', remove 'a' and 'A')
        filtered_polymer = original_polymer.replace(unit, "").replace(unit.upper(), "")
        
        # React the remaining polymer and store length
        length = react_polymer(filtered_polymer)
        results[unit] = length
        print(f"Unit {unit.upper()} removed: resulting length {length}")

    return min(results.values())

if __name__ == "__main__":
    shortest = find_best_reduction(file_path)
    print(f"\nShortest possible length: {shortest}")