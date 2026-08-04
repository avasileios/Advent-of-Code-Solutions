import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def solve_infinite_plants():
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    initial_str = re.search(r'initial state: ([\.#]+)', lines[0]).group(1)
    plants = {i for i, char in enumerate(initial_str) if char == '#'}
    
    rules = {line.split(' => ')[0]: line.split(' => ')[1] for line in lines[1:]}

    prev_sum = 0
    prev_diff = 0
    stable_count = 0
    target = 50_000_000_000

    for gen in range(1, 1000): # 1000 is usually plenty to find the shift
        new_plants = set()
        low, high = min(plants) - 2, max(plants) + 2
        
        for i in range(low, high + 1):
            neighborhood = "".join("#" if j in plants else "." for j in range(i - 2, i + 3))
            if rules.get(neighborhood, '.') == '#':
                new_plants.add(i)
        
        plants = new_plants
        current_sum = sum(plants)
        current_diff = current_sum - prev_sum
        
        # Check if the growth has become linear
        if current_diff == prev_diff:
            stable_count += 1
        else:
            stable_count = 0
            
        # If we see the same difference 10 times in a row, we've hit the slide
        if stable_count > 10:
            remaining_gens = target - gen
            return current_sum + (remaining_gens * current_diff)
        
        prev_sum = current_sum
        prev_diff = current_diff

if __name__ == "__main__":
    result = solve_infinite_plants()
    print(f"The sum after 50 billion generations is: {result}")