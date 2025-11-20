import os
import re
import math
from itertools import combinations

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

def parse_and_validate_by_column(filepath):
    """
    Reads the data into a grid and validates triangles by reading triplets 
    vertically (column by column).
    
    Returns:
        int: The total count of possible triangles.
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
        
    # 1. Parse the entire input into a 2D list of integer lengths
    # We assume each line has exactly three side lengths separated by whitespace.
    parsed_grid = []
    
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            try:
                parsed_grid.append([int(p) for p in parts])
            except ValueError:
                continue
        # Note: If lines have variable numbers of elements, this approach fails. 
        # Assuming fixed 3 columns per line.

    if not parsed_grid:
        return 0
        
    ROWS = len(parsed_grid)
    
    # 2. Iterate by column, processing groups of three rows
    
    # We process in vertical chunks of 3 rows: R, R+1, R+2
    for r in range(0, ROWS, 3):
        
        # Ensure we have at least three rows left to process the triplet
        if r + 2 >= ROWS:
            break
            
        # We always have 3 columns (C=0, C=1, C=2)
        for c in range(3):
            
            # The three side lengths forming the vertical triangle are:
            a = parsed_grid[r][c]       # Top row
            b = parsed_grid[r + 1][c]   # Middle row
            c_side = parsed_grid[r + 2][c] # Bottom row
            
            if is_valid_triangle(a, b, c_side):
                valid_count += 1
                
    return valid_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting triangle validation (Part Two - Column Reading) using data from: {os.path.abspath(input_file)}\n")
    
    final_count = parse_and_validate_by_column(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: TOTAL NUMBER OF POSSIBLE TRIANGLES (Reading by Column):")
    print(f"SCORE: {final_count}")
    print("="*50)