import os

def solve_stream_puzzle(filepath):
    """
    Parses the character stream to calculate the total score of all groups (P1) 
    and the count of non-canceled characters within garbage (P2).
    """
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            stream = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return 0, 0
    
    group_depth = 0
    total_score = 0
    garbage_char_count = 0 # NEW: Counter for Part 2
    in_garbage = False
    i = 0
    N = len(stream)
    
    while i < N:
        char = stream[i]
        
        if in_garbage:
            # --- INSIDE GARBAGE LOGIC ---
            
            if char == '!':
                # Cancellation: Skip this character AND the next one.
                # Do not count '!' or the canceled character towards garbage_char_count.
                i += 2
                continue
            
            elif char == '>':
                # End of garbage (don't count '>')
                in_garbage = False
                i += 1
                continue
            
            else:
                # Any other character inside garbage is a non-canceled, non-bracket character.
                garbage_char_count += 1
                
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
                # Start of garbage (don't count '<')
                in_garbage = True
                
            # Characters like ',' are ignored outside garbage/groups.
            
        i += 1
        
    # Return both results
    return total_score, garbage_char_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting stream analysis using data from: {os.path.abspath(input_file)}\n")
    
    score_p1, count_p2 = solve_stream_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART 1: TOTAL SCORE FOR ALL GROUPS:")
    print(f"SCORE: {score_p1}")
    print("-" * 50)
    print("PART 2: TOTAL NON-CANCELED CHARACTERS WITHIN GARBAGE:")
    print(f"SCORE: {count_p2}")
    print("="*50)