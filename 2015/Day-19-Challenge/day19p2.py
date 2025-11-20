import os
import re

def parse_input(filepath):
    """
    Reads the file, separating replacement rules from the starting molecule.
    
    Returns:
        tuple: (rules: list of (old, new) strings, start_molecule: str)
    """
    rules = []
    start_molecule = ""
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return None, None
        
    in_rules_section = True
    
    for line in lines:
        if not line:
            # Blank line separates rules from molecule
            in_rules_section = False
            continue
            
        if in_rules_section:
            parts = line.split(" => ")
            if len(parts) == 2:
                rules.append((parts[0].strip(), parts[1].strip()))
        else:
            # The last non-empty line is the starting molecule
            start_molecule = line.strip()
            
    return rules, start_molecule

def solve_calibration_puzzle(filepath):
    """
    (Part 1) Calculates the number of distinct molecules that can be generated 
    in one step from the starting molecule.
    """
    rules, start_molecule = parse_input(filepath)
    
    if not rules or not start_molecule:
        print("Error: Could not parse replacement rules or starting molecule.")
        return 0
        
    # Set to store all unique resulting molecules
    distinct_molecules = set()
    
    # 1. Iterate through each rule (Old => New)
    for old, new in rules:
        N_old = len(old)
        N_start = len(start_molecule)
        
        # 2. Iterate through all possible starting positions (i) in the molecule
        for i in range(N_start - N_old + 1):
            
            if start_molecule[i : i + N_old] == old:
                
                # 3. Generate the new molecule
                prefix = start_molecule[:i]
                suffix = start_molecule[i + N_old:]
                new_molecule = prefix + new + suffix
                
                # 4. Add the new molecule to the set
                distinct_molecules.add(new_molecule)
                
    return len(distinct_molecules)

def solve_fabrication_puzzle(filepath):
    """
    (Part 2) Finds the fewest number of steps to reduce the medicine molecule 
    to a single electron 'e' using the reverse greedy approach.
    """
    rules, medicine_molecule = parse_input(filepath)
    
    if not rules or not medicine_molecule:
        print("Error: Could not parse replacement rules or starting molecule.")
        return 0
        
    # 1. Create Reverse Rules (New => Old)
    # The map stores {New_Molecule: Old_Molecule}
    reverse_rules = {}
    for old, new in rules:
        # We only care about the first rule for a given replacement source (new)
        # However, for robustness, we sort the new parts by length (longest first)
        reverse_rules[new] = old
        
    # Convert rules to a list of (new, old) tuples, sorted by length of 'new' (descending)
    # This ensures the longest possible reduction is always attempted first (Greedy).
    sorted_reverse_rules = sorted(
        reverse_rules.items(), 
        key=lambda item: len(item[0]), 
        reverse=True
    )
    
    current_molecule = medicine_molecule
    steps = 0
    
    print(f"Target reduction: {current_molecule} -> e")
    
    # 2. Iterative Reduction
    # We loop until the molecule is reduced to 'e'
    while current_molecule != 'e':
        
        reduction_found = False
        
        # 3. Apply the longest possible reverse replacement (Greedy)
        for new_segment, old_segment in sorted_reverse_rules:
            
            # Find the FIRST (earliest index) occurrence of the New_Segment in the molecule
            index = current_molecule.find(new_segment)
            
            if index != -1:
                # Reduction found! Apply the replacement.
                
                # New molecule = Prefix + Old Segment + Suffix
                prefix = current_molecule[:index]
                suffix = current_molecule[index + len(new_segment):]
                
                current_molecule = prefix + old_segment + suffix
                steps += 1
                reduction_found = True
                break # Break out of the inner loop (rules) to restart scan on the reduced molecule
        
        # Safety Check: If no reduction was found, and we haven't reached 'e', something is wrong.
        if not reduction_found and current_molecule != 'e':
            print("ERROR: Stuck in reduction. Could not find any valid reverse replacement.")
            return -1

    return steps


# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting molecule fabrication analysis (Part 2 - Fewest Steps) using data from: {os.path.abspath(input_file)}\n")
    
    final_steps = solve_fabrication_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: FEWEST NUMBER OF STEPS TO GO FROM 'e' TO MEDICINE:")
    print(f"SCORE: {final_steps}")
    print("="*50)