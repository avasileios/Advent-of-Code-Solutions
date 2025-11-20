import os
import re

def is_valid_triangle(a: int, b: int, c: int) -> bool:
    """
    Checks if three side lengths can form a valid triangle using the 
    Triangle Inequality Theorem.
    """
    # 1. Sum of the two smallest sides must be greater than the largest side.
    # A faster way is to sort them and check only the largest side.
    sides = sorted([a, b, c])
    
    # Check if the sum of the two smaller sides (sides[0] + sides[1]) 
    # is greater than the largest side (sides[2]).
    return sides[0] + sides[1] > sides[2]
def solve_triangle_puzzle(filepath):
    """
    Reads all listed triangles and counts how many are possible.
    """
    valid_count = 0
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return 0
        
    # Regex to find three numbers (separated by any whitespace) on a single line
    pattern = re.compile(r'(\d+)\s+(\d+)\s+(\d+)')
    
    for line in lines:
        match = pattern.match(line)
        if not match:
            # Try splitting by whitespace if regex fails (handles single/multiple spaces/tabs)
            parts = line.split()
            if len(parts) == 3:
                try:
                    a, b, c = map(int, parts)
                except ValueError:
                    continue
            else:
                continue
        else:
            # Use regex groups
            a, b, c = map(int, match.groups())
        
        if is_valid_triangle(a, b, c):
            valid_count += 1
            
    return valid_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting triangle validation using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_triangle_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF POSSIBLE TRIANGLES:")
    print(f"SCORE: {final_count}")
    print("="*50)