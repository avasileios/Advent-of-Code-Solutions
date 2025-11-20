import os
import re

def solve_checksum_puzzle(filepath):
    """
    Calculates the spreadsheet checksum by finding the difference between the 
    largest and smallest value in each row and summing those differences.
    """
    total_checksum = 0
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Spreadsheet file not found at '{filepath}'")
        return 0
    
    for line in lines:
        # Split by any whitespace and convert parts to integers
        try:
            numbers = [int(p) for p in line.split()]
        except ValueError:
            # Skip rows with invalid data
            print(f"Warning: Skipping row with non-numeric data: {line}")
            continue
            
        if not numbers:
            continue
            
        # Find the difference between max and min
        max_val = max(numbers)
        min_val = min(numbers)
        difference = max_val - min_val
        
        # Add to the running checksum
        total_checksum += difference
        
    return total_checksum

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting spreadsheet checksum calculation using data from: {os.path.abspath(input_file)}\n")
    
    final_checksum = solve_checksum_puzzle(input_file)
    
    print("\n" + "="*50)
    print("THE SPREADSHEET CHECKSUM:")
    print(f"SCORE: {final_checksum}")
    print("="*50)