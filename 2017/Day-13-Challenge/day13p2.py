import os
import re
from typing import Dict, Tuple

def parse_firewall(filepath) -> Dict[int, int]:
    """
    Reads the firewall configuration: {depth: range}.
    """
    firewall = {}
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Firewall file not found at '{filepath}'")
        return {}
        
    for line in lines:
        try:
            depth, range_val = map(int, line.split(':'))
            firewall[depth] = range_val
        except ValueError:
            continue
            
    return firewall

def calculate_severity(delay: int, firewall: Dict[int, int]) -> int:
    """
    Calculates the severity of the trip given a starting delay time.
    Returns 0 if the path is safe (no collisions).
    """
    total_severity = 0
    
    for depth, range_val in firewall.items():
        
        # 1. Calculate the arrival time (T_arrival = delay + depth)
        T_arrival = delay + depth
        
        # 2. Calculate the cycle length: 2 * (Range - 1)
        cycle_length = 2 * (range_val - 1)
        
        # 3. Check caught condition: T_arrival % cycle_length == 0
        if T_arrival % cycle_length == 0:
            
            # Caught! Calculate severity: Depth * Range
            severity = depth * range_val
            total_severity += severity
            # Note: For Part 2, we stop checking immediately if severity > 0 is detected
            # But here we calculate full severity for general use.
            
    return total_severity

def solve_firewall_puzzle_part_2(filepath):
    """
    Finds the minimum non-negative delay time T_delay that results in a 
    trip severity of 0 (no collisions).
    """
    firewall = parse_firewall(filepath)
    if not firewall:
        return 0

    T_delay = 0
    
    print("Starting search for minimum safe delay (T_delay = 0, 1, 2, ...)")

    # Iterate through potential delays indefinitely
    while True:
        # We need a quick way to check if ANY collision occurs.
        # Check all layers for the current delay T_delay
        
        is_safe = True
        
        for depth, range_val in firewall.items():
            T_arrival = T_delay + depth
            cycle_length = 2 * (range_val - 1)
            
            if T_arrival % cycle_length == 0:
                is_safe = False
                break # Collision found at this depth, try next delay
        
        if is_safe:
            # Found the first delay time where no collisions occurred
            return T_delay
        
        # If not safe, increment delay and continue
        T_delay += 1
        
        # Optional Status Check
        if T_delay % 100000 == 0:
            print(f"Checked {T_delay} delays so far...")


# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting firewall minimum delay calculation (Part 2) using data from: {os.path.abspath(input_file)}\n")
    
    # Calculate Part 1 severity first (T_delay = 0)
    severity_p1 = calculate_severity(0, parse_firewall(input_file))

    # Calculate Part 2 minimum safe delay
    min_safe_delay = solve_firewall_puzzle_part_2(input_file)
    
    print("\n" + "="*50)
    print("PART 1: SEVERITY OF THE WHOLE TRIP (Delay = 0):")
    print(f"SCORE: {severity_p1}")
    print("-" * 50)
    print("PART 2: FEWEST NUMBER OF PICONDS YOU NEED TO DELAY:")
    print(f"SCORE: {min_safe_delay}")
    print("="*50)