import os
import re
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def find_intact_claim(path):
    fabric = defaultdict(int)
    claims = [] # Store parsed claims for the second pass
    
    with open(path, 'r') as f:
        for line in f:
            parts = list(map(int, re.findall(r'\d+', line)))
            if not parts:
                continue
            
            # parts = [ID, Left, Top, Width, Height]
            claims.append(parts)
            
            # Pass 1: Fill the fabric map
            cid, left, top, width, height = parts
            for x in range(left, left + width):
                for y in range(top, top + height):
                    fabric[(x, y)] += 1
    
    # Pass 2: Find the claim that has no overlaps
    for cid, left, top, width, height in claims:
        is_pristine = True
        
        for x in range(left, left + width):
            for y in range(top, top + height):
                if fabric[(x, y)] > 1:
                    is_pristine = False
                    break
            if not is_pristine:
                break
        
        if is_pristine:
            return cid # This is the ID of the non-overlapping claim

    return "No intact claim found."

if __name__ == "__main__":
    intact_id = find_intact_claim(file_path)
    print(f"The ID of the only claim that doesn't overlap is: {intact_id}")