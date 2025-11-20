import os
import re

def solve_decompression_puzzle(filepath):
    """
    Calculates the decompressed length of the file using non-recursive 
    decompression (Part 1 logic).
    """
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            # Read all content and remove whitespace
            compressed_data = f.read().strip().replace(' ', '')
    except FileNotFoundError:
        print(f"Error: Compressed data file not found at '{filepath}'")
        return 0
    
    if not compressed_data:
        return 0
        
    decompressed_length = 0
    i = 0
    N = len(compressed_data)
    
    while i < N:
        char = compressed_data[i]
        
        if char == '(':
            # Found the start of a marker. Find the end ')'
            end_marker_index = compressed_data.find(')', i)
            
            if end_marker_index == -1:
                # Malformed marker, treat remaining as literal data
                decompressed_length += (N - i)
                break
                
            # Extract marker content (e.g., "10x2")
            marker_content = compressed_data[i + 1: end_marker_index]
            
            try:
                # Parse L (length) and R (repetitions)
                L_str, R_str = marker_content.split('x')
                L = int(L_str)
                R = int(R_str)
            except ValueError:
                # Malformed marker, treat the marker itself as literal data
                decompressed_length += 1
                i += 1
                continue
                
            # Calculate the length of the repeated section
            repeated_length = L * R
            decompressed_length += repeated_length
            
            # Skip past the marker (to end_marker_index + 1)
            # AND skip past the data referenced by the marker (L characters)
            i = end_marker_index + 1 + L
            
        else:
            # Not a marker, count as a single literal character
            decompressed_length += 1
            i += 1
            
    return decompressed_length

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting non-recursive file decompression analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_length = solve_decompression_puzzle(input_file)
    
    print("\n" + "="*50)
    print("DECOMPRESSED LENGTH OF THE FILE:")
    print(f"SCORE: {final_length}")
    print("="*50)