import os
from itertools import combinations

# Setup path relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def find_prototype_boxes(path):
    with open(path, 'r') as f:
        # Read all IDs into a list, stripping whitespace
        ids = [line.strip() for line in f if line.strip()]

    # Check every possible pair of IDs
    for id1, id2 in combinations(ids, 2):
        # Find the indices where the characters differ
        diff_indices = [i for i in range(len(id1)) if id1[i] != id2[i]]
        
        # We are looking for exactly one difference
        if len(diff_indices) == 1:
            idx = diff_indices[0]
            # Return the string with that one character removed
            return id1[:idx] + id1[idx+1:]

    return "No match found."

result = find_prototype_boxes(file_path)
print(f"The common letters between the two correct box IDs are: {result}")