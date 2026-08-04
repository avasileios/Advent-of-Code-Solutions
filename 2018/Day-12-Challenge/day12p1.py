import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def solve_plants():
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Parse initial state
    initial_match = re.search(r'initial state: ([\.#]+)', lines[0])
    initial_str = initial_match.group(1)
    
    # Store indices of pots with plants
    plants = {i for i, char in enumerate(initial_str) if char == '#'}
    
    # Parse rules: key is the pattern, value is the result
    rules = {}
    for line in lines[1:]:
        pattern, result = line.split(' => ')
        rules[pattern] = result

    # Simulate 20 generations
    for _ in range(20):
        new_plants = set()
        # We check two pots beyond the current leftmost and rightmost plants
        low = min(plants) - 2
        high = max(plants) + 2
        
        for i in range(low, high + 1):
            # Build the 5-pot neighborhood string
            neighborhood = ""
            for j in range(i - 2, i + 3):
                neighborhood += "#" if j in plants else "."
            
            # Apply rule (default to '.' if no rule matches)
            if rules.get(neighborhood, '.') == '#':
                new_plants.add(i)
        
        plants = new_plants

    return sum(plants)

if __name__ == "__main__":
    result = solve_plants()
    print(f"The sum of the numbers of all pots which contain a plant is: {result}")