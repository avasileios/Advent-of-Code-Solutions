import os

# --- Constants ---
LIST_SIZE = 256

def parse_lengths(filepath):
    """
    Reads the comma-separated sequence of lengths from the file.
    """
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            line = f.read().strip()
            # Split by comma and convert to integers
            lengths = [int(p.strip()) for p in line.split(',') if p.strip()]
    except FileNotFoundError:
        print(f"Error: Lengths file not found at '{filepath}'")
        return None
    except ValueError:
        print("Error: Invalid content in lengths file (non-integer).")
        return None
    
    return lengths

def solve_knot_hash_puzzle(filepath):
    """
    Simulates the knot tying process and returns the product of the first two elements.
    """
    lengths = parse_lengths(filepath)
    if lengths is None:
        return 0
        
    # 1. Initialization
    list_of_marks = list(range(LIST_SIZE))
    current_position = 0
    skip_size = 0
    N = LIST_SIZE
    
    print(f"Starting knot hash simulation on list size {N} with {len(lengths)} lengths.")

    # 2. Process each length
    for length in lengths:
        
        # Guard against invalid lengths
        if length > N:
            print(f"Warning: Invalid length {length} ignored.")
            continue
            
        # --- A. Identify the sublist to reverse ---
        
        # Collect the values in the span, handling circular wrap
        sublist_values = []
        for i in range(length):
            index = (current_position + i) % N
            sublist_values.append(list_of_marks[index])
            
        # Reverse the sublist values
        sublist_values.reverse()
        
        # --- B. Replace the reversed sublist back into the main list ---
        
        for i in range(length):
            index = (current_position + i) % N
            list_of_marks[index] = sublist_values[i]
            
        # --- C. Move the current position ---
        # Move forward by (length + skip size)
        current_position = (current_position + length + skip_size) % N
        
        # --- D. Increase the skip size ---
        skip_size += 1
        
    # 3. Final Result: Multiply the first two numbers
    if N < 2:
        return 0
        
    final_product = list_of_marks[0] * list_of_marks[1]
    
    return final_product

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Knot Hash analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_knot_hash_puzzle(input_file)
    
    print("\n" + "="*50)
    print("RESULT OF MULTIPLYING THE FIRST TWO NUMBERS IN THE LIST:")
    print(f"SCORE: {final_score}")
    print("="*50)