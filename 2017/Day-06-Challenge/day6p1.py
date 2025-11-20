import os
import re
from typing import List

# --- Constants ---
# Placeholder for your puzzle input
# Example: 0 2 7 0
# ACTUAL INPUT WILL BE READ FROM FILE
DEFAULT_INPUT = "0 2 7 0" 

def find_max_index(banks: List[int]) -> int:
    """
    Finds the index of the memory bank with the most blocks.
    Ties are won by the lowest-numbered (lowest index) memory bank.
    """
    max_blocks = -1
    max_index = -1
    
    # Iterate through the banks and update max_index if a larger value is found, 
    # or if the values are equal (tie-breaker: lower index wins).
    for i, blocks in enumerate(banks):
        if blocks > max_blocks:
            max_blocks = blocks
            max_index = i
            # No need for tie-breaker logic, as we scan from the start (0), 
            # and the first instance of the max value is guaranteed to be the lowest index.
            
    return max_index

def solve_reallocation_puzzle(filepath: str):
    """
    Simulates the reallocation cycles and counts the steps until a configuration 
    is repeated.
    """
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            # Read single line, split by whitespace, and convert to integer list
            line = f.read().strip()
            banks = [int(p) for p in line.split() if p]
    except FileNotFoundError:
        print(f"Error: Banks file not found at '{filepath}'. Using default example.")
        banks = [int(p) for p in DEFAULT_INPUT.split()]
    except ValueError:
        print("Error: Invalid input format. Using default example.")
        banks = [int(p) for p in DEFAULT_INPUT.split()]
        
    if not banks:
        return 0
        
    N = len(banks)
    
    # visited_states stores the memory bank configurations (as tuples for hashing)
    visited_states = set()
    cycles = 0
    
    print(f"Initial Banks: {banks}")
    
    while tuple(banks) not in visited_states:
        
        # 1. Store the current state (before redistribution) and increment cycle count
        visited_states.add(tuple(banks))
        
        # 2. Find the bank to redistribute from (max blocks, lowest index tie)
        index_to_empty = find_max_index(banks)
        blocks_to_redistribute = banks[index_to_empty]
        
        # 3. Remove all blocks from the chosen bank
        banks[index_to_empty] = 0
        
        # 4. Redistribute blocks one by one
        current_index = index_to_empty
        
        for _ in range(blocks_to_redistribute):
            # Move to the next bank circularly
            current_index = (current_index + 1) % N
            
            # Insert one block
            banks[current_index] += 1
            
        # 5. Loop detection check will occur at the start of the next iteration
        cycles += 1

        # print(f"Cycle {cycles}: {banks}") # Optional: Debugging visualization

    print(f"Loop detected after {cycles} cycles. Final state: {banks}")
    
    return cycles

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting memory bank reallocation simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_cycles = solve_reallocation_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL REDISTRIBUTION CYCLES BEFORE LOOP DETECTION:")
    print(f"SCORE: {final_cycles}")
    print("="*50)