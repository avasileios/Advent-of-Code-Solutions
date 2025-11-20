import os
from collections import Counter

def solve_error_correction_puzzle(filepath):
    """
    Reads the corrupted message signal and determines the original message 
    by finding the most frequent character (Part 1) and least frequent (Part 2)
    character at each position.
    """
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Signal file not found at '{filepath}'")
        return "", ""
    
    if not lines:
        return "", ""
        
    message_length = len(lines[0])
    corrected_message_p1 = [] # Most frequent
    corrected_message_p2 = [] # Least frequent
    
    # 1. Iterate through each position (column)
    for i in range(message_length):
        
        column_chars = [line[i] for line in lines]
        frequencies = Counter(column_chars)
        
        # Sort by count (descending) then by character (ascending)
        sorted_items_desc = sorted(
            frequencies.items(),
            key=lambda item: (-item[1], item[0])
        )

        # Sort by count (ascending) then by character (ascending)
        sorted_items_asc = sorted(
            frequencies.items(),
            key=lambda item: (item[1], item[0])
        )
        
        # Part 1: Most frequent character is the first item in the descending sort
        most_common_char = sorted_items_desc[0][0]
        corrected_message_p1.append(most_common_char)
        
        # Part 2: Least frequent character is the first item in the ascending sort
        least_common_char = sorted_items_asc[0][0]
        corrected_message_p2.append(least_common_char)
        
    return "".join(corrected_message_p1), "".join(corrected_message_p2)

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting error correction analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_message_p1, final_message_p2 = solve_error_correction_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART 1: THE ERROR-CORRECTED VERSION (Most Frequent Character):")
    print(f"SCORE: {final_message_p1}")
    print("-" * 50)
    print("PART 2: THE ORIGINAL MESSAGE (Least Common Character):")
    print(f"SCORE: {final_message_p2}")
    print("="*50)