import os

# The constants for VOWELS and DISALLOWED are no longer needed for Part Two

def check_non_overlapping_pair(s: str) -> bool:
    """
    Checks for a pair of any two letters that appears at least twice 
    in the string without overlapping. (Rule 1)
    
    Example: xyxy (xy), aabcdefgaa (aa), but not aaa.
    """
    N = len(s)
    if N < 4:
        return False
        
    # Iterate through all possible starting pairs (s[i:i+2])
    for i in range(N - 1):
        pair = s[i:i+2]
        
        # Search for this pair again starting from position i + 2 (guarantees no overlap)
        # s.find(pair, start_index)
        if s.find(pair, i + 2) != -1:
            return True
            
    return False

def check_repeat_with_gap(s: str) -> bool:
    """
    Checks for at least one letter which repeats with exactly one letter 
    between them (e.g., xyx, abcdefeghi). (Rule 2)
    """
    N = len(s)
    if N < 3:
        return False
        
    # Check for s[i] == s[i+2]
    for i in range(N - 2):
        if s[i] == s[i+2]:
            return True
            
    return False

def is_nice_string(s: str) -> bool:
    """
    Checks if a string meets both new "nice" properties for Part Two.
    """
    
    # Rule 1: Non-overlapping pair appears at least twice
    if not check_non_overlapping_pair(s):
        return False
        
    # Rule 2: Repeating letter with exactly one letter between them
    if not check_repeat_with_gap(s):
        return False
        
    # If both new rules pass
    return True

def solve_nice_string_puzzle(filepath: str):
    """
    Reads the list of strings and counts how many are "nice" under the new rules.
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
    
    print(f"Starting nice string validation (Part Two) using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_nice_string_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: TOTAL NUMBER OF NICE STRINGS (New Rules):")
    print(f"SCORE: {final_count}")
    print("="*50)