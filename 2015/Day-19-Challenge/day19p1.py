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
    Calculates the number of distinct molecules that can be generated 
    in one step from the starting molecule.
    """
    rules, start_molecule = parse_input(filepath)
    
    if not rules or not start_molecule:
        print("Error: Could not parse replacement rules or starting molecule.")
        return 0
        
    # Set to store all unique resulting molecules
    distinct_molecules = set()
    
    print(f"Starting molecule: {start_molecule}")
    print(f"Total replacement rules: {len(rules)}\n")

    # 1. Iterate through each rule (Old => New)
    for old, new in rules:
        N_old = len(old)
        N_start = len(start_molecule)
        
        # 2. Iterate through all possible starting positions (i) in the molecule
        for i in range(N_start - N_old + 1):
            
            # Check if the 'old' segment matches the molecule starting at index i
            if start_molecule[i : i + N_old] == old:
                
                # 3. Generate the new molecule
                # Molecule = Prefix + New Segment + Suffix
                prefix = start_molecule[:i]
                suffix = start_molecule[i + N_old:]
                
                new_molecule = prefix + new + suffix
                
                # 4. Add the new molecule to the set (sets handle uniqueness automatically)
                distinct_molecules.add(new_molecule)
                
    return len(distinct_molecules)

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting molecule calibration analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_calibration_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF DISTINCT MOLECULES CREATED IN ONE STEP:")
    print(f"SCORE: {final_count}")
    print("="*50)