import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def get_node_value(numbers_iter):
    # 1. Read the header
    child_count = next(numbers_iter)
    metadata_count = next(numbers_iter)
    
    # 2. Process all children first and store their values
    child_values = []
    for _ in range(child_count):
        child_values.append(get_node_value(numbers_iter))
        
    # 3. Read the metadata for the current node
    metadata_entries = []
    for _ in range(metadata_count):
        metadata_entries.append(next(numbers_iter))
        
    # 4. Calculate node value based on children
    if child_count == 0:
        # Case 1: No children, value is sum of metadata
        return sum(metadata_entries)
    else:
        # Case 2: Has children, metadata are indices (1-based)
        node_value = 0
        for index in metadata_entries:
            # Convert to 0-based index for Python list
            list_idx = index - 1
            if 0 <= list_idx < len(child_values):
                node_value += child_values[list_idx]
        return node_value

def solve_root_value(path):
    try:
        with open(path, 'r') as f:
            data = list(map(int, f.read().split()))
        
        numbers_iter = iter(data)
        return get_node_value(numbers_iter)
    except FileNotFoundError:
        return "Error: input.txt not found."

if __name__ == "__main__":
    result = solve_root_value(file_path)
    print(f"The value of the root node is: {result}")
