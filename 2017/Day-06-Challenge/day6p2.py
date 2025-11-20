import os
import re
from typing import List, Dict

# --- Constants ---
# Placeholder for your puzzle input
DEFAULT_INPUT = "0 2 7 0" 

def find_max_index(banks: List[int]) -> int:
    """
    Finds the index of the memory bank with the most blocks.
    Ties are won by the lowest-numbered (lowest index) memory bank.
    """
    max_blocks = -1
    max_index = -1
    
    # We scan from the start (0), so the first instance of the max value 
    # is guaranteed to be the lowest index.
    for i, blocks in enumerate(banks):
        if blocks > max_blocks:
            max_blocks = blocks
            max_index = i
            
    return max_index

def solve_reallocation_puzzle(filepath: str):
    """
    Simulates the reallocation cycles and returns both:
    1. Total steps to reach the first loop (Part 1).
    2. The size of the loop (Part 2).
    """
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            line = f.read().strip()
            banks = [int(p) for p in line.split() if p]
    except FileNotFoundError:
        print(f"Error: Banks file not found at '{filepath}'. Using default example.")
        banks = [int(p) for p in DEFAULT_INPUT.split()]
    except ValueError:
        print("Error: Invalid input format. Using default example.")
        banks = [int(p) for p in DEFAULT_INPUT.split()]
        
    if not banks:
        return 0, 0
        
    N = len(banks)
    
    # Part 1 & 2: seen_states maps {state_tuple: cycle_number_of_first_visit}
    # Note: Cycle 0 is the initial state before any redistribution.
    seen_states: Dict[Tuple, int] = {}
    cycles = 0
    
    print(f"Initial Banks: {banks}")
    
    while tuple(banks) not in seen_states:
        
        # 1. Store the current state and its cycle index
        current_state = tuple(banks)
        seen_states[current_state] = cycles
        
        # 2. Find the bank to redistribute from
        index_to_empty = find_max_index(banks)
        blocks_to_redistribute = banks[index_to_empty]
        
        # 3. Remove all blocks
        banks[index_to_empty] = 0
        
        # 4. Redistribute blocks one by one
        current_index = index_to_empty
        
        for _ in range(blocks_to_redistribute):
            current_index = (current_index + 1) % N
            banks[current_index] += 1
            
        cycles += 1

    # Loop detected!
    
    # Part 1 Result: Total cycles completed to reach the first loop state
    cycles_to_loop_entry = cycles 
    
    # Part 2 Result: Calculate the loop size
    # The current state (tuple(banks)) is the repeating state.
    first_seen_cycle = seen_states[tuple(banks)]
    loop_size = cycles - first_seen_cycle
    
    print(f"Repeating state {tuple(banks)} first seen at cycle {first_seen_cycle}.")
    print(f"Current cycle: {cycles}.")

    return cycles_to_loop_entry, loop_size

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting memory bank reallocation simulation using data from: {os.path.abspath(input_file)}\n")
    
    cycles_p1, cycles_p2 = solve_reallocation_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART 1: TOTAL REDISTRIBUTION CYCLES BEFORE LOOP DETECTION:")
    print(f"SCORE: {cycles_p1}")
    print("-" * 50)
    print("PART 2: SIZE OF THE INFINITE LOOP:")
    print(f"SCORE: {cycles_p2}")
    print("="*50)