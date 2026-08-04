import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def parse_tree(numbers_iter):
    # 1. Read the header
    child_count = next(numbers_iter)
    metadata_count = next(numbers_iter)
    
    total_metadata_sum = 0
    
    # 2. Recursively process all children
    for _ in range(child_count):
        total_metadata_sum += parse_tree(numbers_iter)
        
    # 3. Add current node's metadata
    for _ in range(metadata_count):
        total_metadata_sum += next(numbers_iter)
        
    return total_metadata_sum

def solve_metadata_sum(path):
    with open(path, 'r') as f:
        # Convert the space-separated string into a list of integers
        data = list(map(int, f.read().split()))
    
    # Create an iterator so the recursive calls "consume" the list
    numbers_iter = iter(data)
    
    return parse_tree(numbers_iter)

if __name__ == "__main__":
    result = solve_metadata_sum(file_path)
    print(f"The sum of all metadata entries is: {result}")