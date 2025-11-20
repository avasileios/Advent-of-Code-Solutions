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

def solve_firewall_puzzle(filepath):
    """
    Calculates the severity of the trip if the packet leaves immediately (T=0).
    """
    firewall = parse_firewall(filepath)
    if not firewall:
        print("No firewall data loaded.")
        return 0

    total_severity = 0
    
    # Iterate through all layers in the firewall
    for depth, range_val in firewall.items():
        
        # 1. Calculate the time of arrival (T_arrival = depth)
        T_arrival = depth
        
        # 2. Calculate the cycle length: 2 * (Range - 1)
        # This is the period after which the scanner returns to position 0.
        cycle_length = 2 * (range_val - 1)
        
        # 3. Check caught condition: T_arrival % cycle_length == 0
        if T_arrival % cycle_length == 0:
            
            # Caught! Calculate severity: Depth * Range
            severity = depth * range_val
            total_severity += severity
            # print(f"[CAUGHT] Depth {depth}, Range {range_val}. Severity added: {severity}")
        
    return total_severity

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting firewall severity calculation using data from: {os.path.abspath(input_file)}\n")
    
    final_severity = solve_firewall_puzzle(input_file)
    
    print("\n" + "="*50)
    print("SEVERITY OF THE WHOLE TRIP (Leaving Immediately):")
    print(f"SCORE: {final_severity}")
    print("="*50)