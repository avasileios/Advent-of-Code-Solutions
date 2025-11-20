import os
import re
import json # Used for a sanity check, though not for the main calculation

def solve_json_sum_puzzle(filepath):
    """
    Finds and sums all numbers in a JSON document using regular expressions
    for maximum speed.
    """
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            json_string = f.read().strip()
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{filepath}'")
        return 0
    
    if not json_string:
        print("Input file is empty.")
        return 0

    # Regex to find all numbers (integers, possibly negative, and optional decimals)
    # Pattern: -? matches optional negative sign
    #          \d+ matches one or more digits
    #          (\.\d+)? matches an optional decimal part
    # We only expect integers based on the examples, so we simplify:
    number_pattern = re.compile(r'-?\d+')
    
    total_sum = 0
    
    # Find all matches in the raw JSON string
    matches = number_pattern.findall(json_string)
    
    if not matches:
        print("No numbers found in the document.")
        return 0

    # Convert matches to integers and sum them up
    for num_str in matches:
        try:
            total_sum += int(num_str)
        except ValueError:
            # Should not happen if the regex is correct, but safe measure
            continue
            
    return total_sum

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting JSON number summation using data from: {os.path.abspath(input_file)}\n")
    
    final_sum = solve_json_sum_puzzle(input_file)
    
    print("\n" + "="*50)
    print("SUM OF ALL NUMBERS IN THE DOCUMENT:")
    print(f"SCORE: {final_sum}")
    print("="*50)