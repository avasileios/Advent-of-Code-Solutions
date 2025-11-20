import os
import re
import json 

def recursive_sum_filter(data):
    """
    Recursively sums all numbers in the data structure, ignoring any object 
    (dictionary) that contains the value "red". This filter does not apply to arrays.
    """
    total_sum = 0
    
    # Check if the data is a dictionary (JSON object)
    if isinstance(data, dict):
        
        # Rule Check: If the object contains the value "red", ignore it entirely.
        if "red" in data.values():
            return 0 # Ignore this object and all its contents
        
        # If no "red", recursively sum all values in the dictionary
        for value in data.values():
            total_sum += recursive_sum_filter(value)
            
    # Check if the data is a list (JSON array)
    elif isinstance(data, list):
        # Rule: Arrays are processed normally, even if they contain "red".
        for item in data:
            total_sum += recursive_sum_filter(item)
            
    # Check if the data is a number
    elif isinstance(data, (int, float)):
        total_sum += data
        
    # All other types (strings, boolean, null) are ignored (return 0)
    
    return total_sum

def solve_json_sum_puzzle(filepath):
    """
    Loads the JSON document and calculates the sum of numbers based on 
    the Part 2 filter rule.
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

    try:
        # Load the entire document structure
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON document: {e}")
        return 0

    # Run the recursive solver with the filter
    final_sum = recursive_sum_filter(data)
            
    return final_sum

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting JSON number summation (Part Two Filter) using data from: {os.path.abspath(input_file)}\n")
    
    final_sum = solve_json_sum_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: SUM OF ALL NUMBERS (Excluding 'red' objects):")
    print(f"SCORE: {final_sum}")
    print("="*50)