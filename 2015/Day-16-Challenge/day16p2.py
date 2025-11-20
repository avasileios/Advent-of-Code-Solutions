import os
import re

# The target readings from the MFCSAM ticker tape
TARGET_READINGS = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1
}

def parse_sues(filepath):
    """
    Reads the list of Aunt Sue data from the file.
    
    Returns:
        dict: A dictionary where key is the Sue number (int) and value is 
              a dict of known properties {property: count}.
    """
    sues = {}
    
    try:
        # Robust file path construction
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return {}
        
    # Regex to capture the structure: Sue X: prop1: count1, prop2: count2, ...
    pattern = re.compile(r'Sue (\d+): (.+)')
    property_pattern = re.compile(r'(\w+):\s*(\d+)')

    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        sue_number = int(match.group(1))
        properties_str = match.group(2)
        
        sue_properties = {}
        
        # Parse the comma-separated properties within the line
        for prop_match in property_pattern.finditer(properties_str):
            prop_name = prop_match.group(1)
            prop_count = int(prop_match.group(2))
            sue_properties[prop_name] = prop_count
            
        sues[sue_number] = sue_properties
        
    return sues

def find_matching_sue(sues):
    """
    Finds the single Aunt Sue whose known properties do not contradict the 
    MFCSAM target readings, using the new range rules for certain compounds.
    """
    
    for sue_number, properties in sues.items():
        is_match = True
        
        # Check every known property against the target readings
        for prop_name, prop_count in properties.items():
            
            if prop_name not in TARGET_READINGS:
                continue # Should not happen, but safe to skip unknown properties
                
            target_count = TARGET_READINGS[prop_name]
            
            # --- APPLY PART TWO RANGE RULES ---
            
            if prop_name in ["cats", "trees"]:
                # Rule: Greater than target value
                if prop_count <= target_count:
                    is_match = False
                    break
            
            elif prop_name in ["pomeranians", "goldfish"]:
                # Rule: Fewer than target value
                if prop_count >= target_count:
                    is_match = False
                    break
            
            else:
                # Rule: Exact match for all other properties
                if prop_count != target_count:
                    is_match = False
                    break
        
        if is_match:
            # If no contradictions were found, this is the Aunt Sue.
            return sue_number
            
    return None # No matching Sue found

def solve_aunt_sue_puzzle(filepath):
    """Main function to run the analysis."""
    
    sues = parse_sues(filepath)
    if not sues:
        print("No Aunt Sue data loaded.")
        return 0
        
    print(f"Total Aunt Sues loaded: {len(sues)}")
    
    winning_sue_number = find_matching_sue(sues)
    
    return winning_sue_number

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Aunt Sue analysis (Part Two - Range Filter) using data from: {os.path.abspath(input_file)}\n")
    
    final_sue = solve_aunt_sue_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: THE NUMBER OF THE REAL AUNT SUE (Range Filter):")
    print(f"SCORE: {final_sue}")
    print("="*50)