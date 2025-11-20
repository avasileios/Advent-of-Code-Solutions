import os
import re

def parse_marker(s, start_index):
    """
    Parses a marker starting at start_index (e.g., (10x2)).
    Returns (L, R, end_of_marker_index) or None if malformed.
    """
    end_marker_index = s.find(')', start_index)
    
    if end_marker_index == -1:
        return None
        
    marker_content = s[start_index + 1: end_marker_index]
    
    try:
        L_str, R_str = marker_content.split('x')
        L = int(L_str)
        R = int(R_str)
        return L, R, end_marker_index
    except ValueError:
        return None

def calculate_recursive_length(s: str) -> int:
    """
    Calculates the decompressed length of the string s recursively.
    This handles version two of the format where markers are decompressed.
    """
    total_length = 0
    i = 0
    N = len(s)
    
    while i < N:
        char = s[i]
        
        if char == '(':
            # Found the start of a marker.
            marker_info = parse_marker(s, i)
            
            if marker_info is None:
                # Malformed marker, treat remaining as literal data
                total_length += (N - i)
                break
                
            L, R, end_marker_index = marker_info
            
            # The data segment referenced by the marker (L characters long)
            data_start = end_marker_index + 1
            data_end = data_start + L
            
            # Ensure the referenced data is within the bounds of the current segment
            if data_end > N:
                # This should not happen with valid input but prevents errors
                total_length += (N - i)
                break
            
            data_segment = s[data_start: data_end]
            
            # CRITICAL STEP: Recursively calculate the length of the data segment
            length_of_data_segment = calculate_recursive_length(data_segment)
            
            # Add the repeated length to the total
            total_length += length_of_data_segment * R
            
            # Skip past the marker and the data referenced by the marker (L characters)
            i = data_end
            
        else:
            # Not a marker, count as a single literal character
            total_length += 1
            i += 1
            
    return total_length

def solve_decompression_puzzle(filepath):
    """
    Calculates the decompressed length of the file using recursive decompression (Part 2 logic).
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
        
    # Start the recursive calculation from the entire compressed data
    final_length = calculate_recursive_length(compressed_data)
            
    return final_length

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting recursive file decompression analysis (Part 2) using data from: {os.path.abspath(input_file)}\n")
    
    final_length = solve_decompression_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: DECOMPRESSED LENGTH OF THE FILE (Recursive Format):")
    print(f"SCORE: {final_length}")
    print("="*50)