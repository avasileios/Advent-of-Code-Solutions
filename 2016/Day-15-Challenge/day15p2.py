import os
import re

# Total number of positions is P
# Initial position (at T=0) is S
# Disc index (1-based) is D

def parse_discs(filepath):
    """
    Reads disc data and extracts (positions, initial_position, disc_index).
    
    Returns:
        list: List of (P, S, D) tuples.
    """
    discs = []
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Disc file not found at '{filepath}'")
        return []
    
    # Regex to capture the required parts: Disc #D has P positions; at time=0, it is at position S.
    pattern = re.compile(
        r'Disc #(\d+)\s+has\s+(\d+)\s+positions;\s+at time=0,\s+it is at position\s+(\d+)\.'
    )
    
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        # Group 1 (D): Disc index, Group 2 (P): Positions, Group 3 (S): Start Position
        D = int(match.group(1))
        P = int(match.group(2))
        S = int(match.group(3))
        
        discs.append((P, S, D))
        
    return discs

def solve_sculpture_puzzle(filepath):
    """
    Finds the minimum non-negative time T that satisfies the modular condition 
    for all discs, including the new Part Two disc.
    """
    discs = parse_discs(filepath)
    if not discs:
        print("No disc data parsed.")
        return 0

    # --- PART TWO MODIFICATION ---
    
    # 1. Add the new disc to the system.
    num_original_discs = len(discs)
    D_new = num_original_discs + 1
    P_new = 11  # 11 positions
    S_new = 0   # starts at position 0
    
    discs.append((P_new, S_new, D_new))
    print(f"Added new disc #{D_new} (Positions: {P_new}, Start: {S_new}).")

    # 2. Simplify the Modular Constraints
    # We want T = R_i (mod P_i), where R_i = -(S_i + D_i) mod P_i
    
    # Calculate the remainder R_i and modulus P_i for each disc
    constraints = []
    for P, S, D in discs:
        # R = -(S + D)
        remainder = -(S + D) % P
        constraints.append((P, remainder))
        
    # Optimization: Sort constraints by modulus (P) descending, 
    # to iterate by the largest and most restrictive constraint first.
    constraints.sort(key=lambda x: x[0], reverse=True)

    # 3. Iterative Search (Optimized Step-and-Check / CRT)
    
    # Start with the modulus of the most restrictive constraint
    step = 1 
    current_time = 0
    
    # We must import math inside the function scope for the next tool call
    import math
    
    for P_i, R_i in constraints:
        
        # Search for the next time 'T' starting from 'current_time' that satisfies:
        # T === R_i (mod P_i)
        
        while current_time % P_i != R_i:
            current_time += step
        
        # Once current_time satisfies the i-th constraint, update the step size 
        # to the LCM (which ensures the previously satisfied constraints remain true).
        lcm = (step * P_i) // math.gcd(step, P_i)
        step = lcm # New step size is the LCM of all moduli processed so far.


    # 4. Final Check (Return the current time)
    return current_time

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting kinetic sculpture time optimization (Part Two) using data from: {os.path.abspath(input_file)}\n")
    
    final_time = solve_sculpture_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: FIRST TIME YOU CAN PRESS THE BUTTON TO GET A CAPSULE (New Disc Added):")
    print(f"SCORE: {final_time}")
    print("="*50)