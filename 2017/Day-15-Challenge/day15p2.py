import os
import re

# --- Constants ---
DIVISOR = 2147483647
FACTOR_A = 16807
FACTOR_B = 48271
TOTAL_PAIRS = 5000000 # Updated to 5 million pairs
BIT_MASK = 65535      # 2^16 - 1 (for checking the lowest 16 bits)

# --- NEW FILTER CRITERIA ---
FILTER_A = 4
FILTER_B = 8

def parse_start_values(filepath):
    """
    Reads the starting values for Generator A and Generator B.
    """
    # Note: Based on standard AoC input format, we assume the file contains 
    # the lines "Generator A starts with X" and "Generator B starts with Y".
    # Defaults to example values if parsing fails
    start_a, start_b = 65, 8921 
    
    try:
        # Robust file path reading
        absolute_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(absolute_filepath, 'r') as f:
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
    Simulates the generator process for 5 million pairs using the new 
    divisibility filtering criteria.
    """
    start_a, start_b = parse_start_values(filepath)
    
    current_a = start_a
    current_b = start_b
    match_count = 0
    
    print(f"Starting A: {start_a}, Starting B: {start_b}")
    print(f"Simulating up to {TOTAL_PAIRS} filtered pairs...")

    # Generator A loop
    def generate_filtered_a(initial_a):
        val = initial_a
        while True:
            val = (val * FACTOR_A) % DIVISOR
            if val % FILTER_A == 0:
                yield val

    # Generator B loop
    def generate_filtered_b(initial_b):
        val = initial_b
        while True:
            val = (val * FACTOR_B) % DIVISOR
            if val % FILTER_B == 0:
                yield val

    # Initialize the generators
    gen_a = generate_filtered_a(start_a)
    gen_b = generate_filtered_b(start_b)

    # 1. Compare 5 million pairs
    for i in range(TOTAL_PAIRS):
        
        # 2. Get the next *filtered* value from each generator
        current_a = next(gen_a)
        current_b = next(gen_b)
        
        # 3. Check for match in the lowest 16 bits
        if (current_a & BIT_MASK) == (current_b & BIT_MASK):
            match_count += 1
            
    return match_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting generator matching simulation (Part 2 - Filtered) using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_generator_puzzle(input_file)
    
    print("\n" + "="*50)
    print(f"PART TWO: JUDGE'S FINAL COUNT AFTER {TOTAL_PAIRS} FILTERED PAIRS:")
    print(f"SCORE: {final_count}")
    print("="*50)