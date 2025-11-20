import os
import re
import math
from itertools import combinations

def parse_weights(filepath):
    """
    Reads package weights from the input file.
    
    Returns:
        list: A list of integer package weights.
    """
    weights = []
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Weights file not found at '{filepath}'")
        return []
    
    for line in lines:
        try:
            weights.append(int(line))
        except ValueError:
            print(f"Warning: Skipping non-integer line: {line}")
            continue
            
    return weights

def calculate_qe(group: tuple) -> int:
    """
    Calculates the Quantum Entanglement (product of weights) for a group.
    """
    qe = 1
    for weight in group:
        qe *= weight
    return qe

def solve_sleigh_puzzle(filepath):
    """
    Finds the lowest Quantum Entanglement (QE) for Group 1, prioritized by 
    minimum size and then minimum QE.
    """
    weights = parse_weights(filepath)
    if not weights:
        print("No weights loaded.")
        return 0

    total_weight = sum(weights)
    
    # 1. Check for divisibility and determine target weight
    if total_weight % 3 != 0:
        print(f"Error: Total weight ({total_weight}) is not divisible by 3. Cannot balance.")
        return 0
        
    W_target = total_weight // 3
    
    print(f"Total packages: {len(weights)}. Total weight: {total_weight}.")
    print(f"Target weight per group: {W_target}")
    
    min_size = float('inf')
    min_qe = float('inf')
    
    # 2. Search by size (N)
    # We search from size 1 up to (N/3) packages, checking for the first minimum size.
    
    # Sort weights descendingly. This is generally good practice but not strictly required for combinations.
    # We sort them ASCENDINGLY here, as it helps in finding the minimum QE sooner 
    # among groups of the same size if the puzzle input structure favors it.
    weights.sort() 
    
    for size in range(1, len(weights) + 1):
        
        # Optimization: If we found the minimum size, we only continue checking 
        # combinations of this size, and then we stop.
        if size > min_size:
            break
            
        found_match_at_current_size = False
        
        # 3. Generate all combinations of the current size
        for group1 in combinations(weights, size):
            if sum(group1) == W_target:
                
                # Check for Group 1's size
                if size < min_size:
                    # Found a NEW minimum size! Reset QE tracking.
                    min_size = size
                    min_qe = calculate_qe(group1)
                    found_match_at_current_size = True
                    
                elif size == min_size:
                    # Found another way to achieve the current minimum size. 
                    # Only update QE if the current QE is smaller.
                    current_qe = calculate_qe(group1)
                    min_qe = min(min_qe, current_qe)
                    
                    found_match_at_current_size = True

        # Stop searching larger sizes as soon as the first match is found.
        if min_size < float('inf') and found_match_at_current_size and size == min_size:
            # We are guaranteed to have found the absolute minimum size (N_min)
            # and the absolute minimum QE for that size (min_qe).
            break 
            
    return min_qe if min_qe != float('inf') else 0

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Sleigh Balancer analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_sleigh_puzzle(input_file)
    
    print("\n" + "="*50)
    print("QUANTUM ENTANGLEMENT OF THE FIRST GROUP IN THE IDEAL CONFIGURATION:")
    print(f"SCORE: {final_score}")
    print("="*50)