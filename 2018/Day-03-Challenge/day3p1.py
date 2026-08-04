import os
import re
from collections import defaultdict

# Path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def solve_fabric_overlaps(path):
    # fabric[(x, y)] will store how many claims cover that inch
    fabric = defaultdict(int)
    
    with open(path, 'r') as f:
        for line in f:
            # Parse numbers: #ID @ L,T: WxH
            # matches: [ID, Left, Top, Width, Height]
            parts = re.findall(r'\d+', line)
            if not parts:
                continue
            
            _, left, top, width, height = map(int, parts)
            
            # Mark every square inch covered by this claim
            for x in range(left, left + width):
                for y in range(top, top + height):
                    fabric[(x, y)] += 1
    
    # Count how many inches have 2 or more claims
    overlap_count = sum(1 for count in fabric.values() if count >= 2)
    return overlap_count

if __name__ == "__main__":
    result = solve_fabric_overlaps(file_path)
    print(f"Total square inches with two or more claims: {result}")