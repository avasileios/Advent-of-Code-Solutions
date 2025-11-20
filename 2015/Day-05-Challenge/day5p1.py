import os

VOWELS = "aeiou"
DISALLOWED = ["ab", "cd", "pq", "xy"]

def is_nice_string(s: str) -> bool:
    """
    Checks if a string meets all three "nice" properties.
    """
    
    # --- Rule 1: Contains at least three vowels ---
    vowel_count = 0
    for char in s:
        if char in VOWELS:
            vowel_count += 1
    
    if vowel_count < 3:
        return False
        
    # --- Rule 2: Contains at least one letter that appears twice in a row ---
    has_double_letter = False
    for i in range(len(s) - 1):
        if s[i] == s[i+1]:
            has_double_letter = True
            break
            
    if not has_double_letter:
        return False
        
    # --- Rule 3: Does not contain the disallowed substrings (ab, cd, pq, or xy) ---
    for bad_pair in DISALLOWED:
        if bad_pair in s:
            return False
            
    # If all checks pass
    return True

def solve_nice_string_puzzle(filepath: str):
    """
    Reads the list of strings and counts how many are "nice".
    """
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            strings = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return 0
        
    if not strings:
        print("No strings found in the input file.")
        return 0
        
    nice_count = 0
    
    for s in strings:
        if is_nice_string(s):
            nice_count += 1
            
    return nice_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting nice string validation using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_nice_string_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF NICE STRINGS:")
    print(f"SCORE: {final_count}")
    print("="*50)