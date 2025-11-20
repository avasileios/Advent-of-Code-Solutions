import os

def solve_stream_puzzle(filepath):
    """
    Parses the character stream to calculate the total score of all groups, 
    handling garbage and cancellation rules.
    """
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            stream = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return 0
    
    group_depth = 0
    total_score = 0
    in_garbage = False
    i = 0
    N = len(stream)
    
    while i < N:
        char = stream[i]
        
        if in_garbage:
            # --- INSIDE GARBAGE LOGIC ---
            
            if char == '!':
                # Cancellation: Ignore this character AND the next one.
                i += 2
                continue
            
            elif char == '>':
                # End of garbage
                in_garbage = False
                i += 1
                continue
                
            # If any other character, it is treated as part of the garbage, 
            # and we move to the next character without specific action.
            
        else:
            # --- OUTSIDE GARBAGE LOGIC ---
            
            if char == '{':
                # Start of a new group. Increase depth and add new depth to score.
                group_depth += 1
                total_score += group_depth
                
            elif char == '}':
                # End of a group. Decrease depth.
                group_depth -= 1
                
            elif char == '<':
                # Start of garbage
                in_garbage = True
                
            # Characters like ',' are ignored outside garbage/groups.
            
        i += 1
        
    # The final group depth must be 0 for a valid stream, but the puzzle 
    # assumes valid structure, so we just return the total_score.
    return total_score

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting stream analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_stream_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL SCORE FOR ALL GROUPS:")
    print(f"SCORE: {final_score}")
    print("="*50)