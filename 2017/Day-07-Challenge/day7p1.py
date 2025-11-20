import os
import re
from typing import Set, Dict

def parse_towers(filepath) -> tuple[Set[str], Set[str], Dict[str, int]]:
    """
    Reads the tower structure data.
    
    Returns:
        tuple: (all_programs, all_children, weights)
    """
    all_programs = set()
    all_children = set()
    weights = {}
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return set(), set(), {}
        
    # Regex to capture the structure: Name (Weight) -> Children List
    pattern = re.compile(r'(\w+)\s+\((\d+)\)(?:\s+->\s+(.*))?')

    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        name = match.group(1)
        weight = int(match.group(2))
        children_str = match.group(3)
        
        # 1. Add name to the set of all programs
        all_programs.add(name)
        weights[name] = weight
        
        # 2. Process children if they exist
        if children_str:
            children = [c.strip() for c in children_str.split(',')]
            all_children.update(children)
            
    return all_programs, all_children, weights

def solve_tower_root_puzzle(filepath):
    """
    Finds the name of the program that is never held up (the root).
    """
    all_programs, all_children, _ = parse_towers(filepath)
    
    if not all_programs:
        print("No program data parsed.")
        return ""
        
    # The bottom program is the element in all_programs that is NOT in all_children.
    root_set = all_programs.difference(all_children)
    
    if len(root_set) != 1:
        print(f"Error: Found {len(root_set)} potential root programs. Check input format.")
        return f"Multiple roots found: {root_set}"
        
    return list(root_set)[0]

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting tower structure analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_root_name = solve_tower_root_puzzle(input_file)
    
    print("\n" + "="*50)
    print("NAME OF THE BOTTOM PROGRAM (THE ROOT):")
    print(f"SCORE: {final_root_name}")
    print("="*50)