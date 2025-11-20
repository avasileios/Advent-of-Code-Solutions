import os
import re

def solve_checksum_puzzle(filepath):
    """
    Calculates the spreadsheet checksum for both Part 1 (Max-Min Difference) 
    and Part 2 (Evenly Divisible Pairs).
    """
    total_checksum_p1 = 0
    total_checksum_p2 = 0
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Spreadsheet file not found at '{filepath}'")
        return 0, 0
    
    for line in lines:
        try:
            # Split by any whitespace and convert parts to integers
            numbers = [int(p) for p in line.split()]
        except ValueError:
            # Skip rows with invalid data
            print(f"Warning: Skipping row with non-numeric data: {line}")
            continue
            
        if not numbers:
            continue
            
        # --- Part 1: Max - Min Difference ---
        max_val = max(numbers)
        min_val = min(numbers)
        total_checksum_p1 += (max_val - min_val)
        
        # --- Part 2: Evenly Divisible Pair ---
        
        found_division_result = 0
        
        # Nested loops to check every unique ordered pair (A, B)
        # We use indices to ensure we don't divide a number by itself (i != j)
        N = len(numbers)
        for i in range(N):
            for j in range(N):
                # Rule: Must be two different numbers (i != j)
                if i == j:
                    continue
                
                num_a = numbers[i]
                num_b = numbers[j]
                
                # Check if num_a evenly divides num_b
                if num_b % num_a == 0:
                    # Found the pair where num_a divides num_b
                    found_division_result = num_b // num_a
                    # Since the puzzle guarantees only one such pair per row, we can break both loops
                    # We break the inner loop (j) and rely on the outer loop (i) breaking next.
                    # A more explicit flag is needed to break both, but breaking inner and continuing 
                    # outer is simpler if we trust the guarantee.
                    break 
            
            if found_division_result != 0:
                break # Break the outer loop (i)
                
        total_checksum_p2 += found_division_result
        
    return total_checksum_p1, total_checksum_p2

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting spreadsheet checksum calculation (Part 2) using data from: {os.path.abspath(input_file)}\n")
    
    checksum_p1, checksum_p2 = solve_checksum_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART 1: MAX-MIN CHECKSUM:")
    print(f"SCORE: {checksum_p1}")
    print("-" * 50)
    print("PART 2: SUM OF EACH ROW'S EVENLY DIVISIBLE RESULT:")
    print(f"SCORE: {checksum_p2}")
    print("="*50)