import os
from collections import Counter

# This gets the directory where the script itself is saved
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def calculate_checksum(path):
    twos_count = 0
    threes_count = 0
    
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            counts = set(Counter(line).values()) # Using a set makes lookups fast
            if 2 in counts:
                twos_count += 1
            if 3 in counts:
                threes_count += 1
                
    return twos_count * threes_count

print(f"The checksum for the box IDs is: {calculate_checksum(file_path)}")