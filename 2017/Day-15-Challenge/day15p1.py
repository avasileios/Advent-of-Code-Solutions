import os
import re

# --- Constants ---
DIVISOR = 2147483647
FACTOR_A = 16807
FACTOR_B = 48271
TOTAL_PAIRS = 40000000 # 40 million
BIT_MASK = 65535      # 2^16 - 1 (for checking the lowest 16 bits)

def parse_start_values(filepath):
    """
    Reads the starting values for Generator A and Generator B.
    """
    # Note: Based on standard AoC input format, we assume the file contains 
    # the lines "Generator A starts with X" and "Generator B starts with Y".
    start_a, start_b = 65, 8921 # Defaults to example values if parsing fails
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if "Generator A starts with" in line:
                    start_a = int(line.split()[-1])
                elif "Generator B starts with" in line:
                    start_b = int(line.split()[-1])
    except FileNotFoundError:
        print(f"Warning: Input file not found. Using example starting values (A={start_a}, B={start_b}).")
        
    return start_a, start_b

def solve_generator_puzzle(filepath):
    """
    Simulates the generator process for 40 million pairs and counts the matches.
    """
    start_a, start_b = parse_start_values(filepath)
    
    current_a = start_a
    current_b = start_b
    match_count = 0
    
    print(f"Starting A: {start_a}, Starting B: {start_b}")
    print(f"Simulating {TOTAL_PAIRS} pairs...")

    for i in range(TOTAL_PAIRS):
        
        # 1. Generate next value for A
        current_a = (current_a * FACTOR_A) % DIVISOR
        
        # 2. Generate next value for B
        current_b = (current_b * FACTOR_B) % DIVISOR
        
        # 3. Check for match in the lowest 16 bits
        # V % 2^16 is equivalent to V & 0xFFFF
        if (current_a & BIT_MASK) == (current_b & BIT_MASK):
            match_count += 1
            
    return match_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting generator matching simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_generator_puzzle(input_file)
    
    print("\n" + "="*50)
    print(f"JUDGE'S FINAL COUNT AFTER {TOTAL_PAIRS} PAIRS:")
    print(f"SCORE: {final_count}")
    print("="*50)