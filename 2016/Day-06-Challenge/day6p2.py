import os
from collections import Counter

def solve_error_correction_puzzle(filepath):
    """
    Reads the corrupted message signal and determines the original message 
    by finding the least frequent character at each position (Modified Code).
    """
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Signal file not found at '{filepath}'")
        return ""
    
    if not lines:
        return ""
        
    # Determine the length of the message (number of columns)
    message_length = len(lines[0])
    
    # List to hold the final corrected message characters
    original_message = []
    
    # 1. Iterate through each position (column)
    for i in range(message_length):
        
        # 2. Extract all characters for the current column
        column_chars = [line[i] for line in lines]
        
        # 3. Find the least frequent character
        
        frequencies = Counter(column_chars)
        
        # Find the character with the minimum count.
        # We sort the items: first by count (ascending: item[1]), 
        # and second by character (ascending: item[0]) as a stable tie-breaker.
        
        least_common_char = sorted(
            frequencies.items(),
            key=lambda item: (item[1], item[0]) # Sort by (count, char) ascending
        )[0][0] # Take the character (index 0) of the first item in the sorted list
        
        original_message.append(least_common_char)
        
    return "".join(original_message)

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting error correction analysis (Part Two - Least Common) using data from: {os.path.abspath(input_file)}\n")
    
    final_message = solve_error_correction_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: THE ORIGINAL MESSAGE (Least Common Character):")
    print(f"SCORE: {final_message}")
    print("="*50)