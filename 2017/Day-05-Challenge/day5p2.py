import os
import sys

def parse_offsets(filepath: str) -> list[int]:
    """
    Reads the list of jump offsets, one per line.
    """
    offsets = []
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        for line in lines:
            try:
                offsets.append(int(line))
            except ValueError:
                continue
    except FileNotFoundError:
        print(f"Error: Jump offsets file not found at '{filepath}'")
        return []
        
    return offsets

def solve_jump_maze(filepath: str) -> int:
    """
    Simulates the relative jumps with the new conditional offset rule and counts 
    the steps until the IP moves outside the program list.
    """
    # Load offsets into a mutable list
    offsets = parse_offsets(filepath)
    if not offsets:
        return 0
        
    ip = 0 # Instruction Pointer (starts at index 0)
    steps = 0
    N = len(offsets)
    
    # We use a safety break, though the program should halt naturally.
    # The required steps for Part 2 is often much larger than Part 1, so increase limit.
    MAX_STEPS = 50000000 
    
    while 0 <= ip < N and steps < MAX_STEPS:
        
        # 1. Get the current offset value
        jump_offset = offsets[ip]
        
        # 2. Update Rule: Conditional Offset Change
        if jump_offset >= 3:
            # If offset was three or more, decrease it by 1.
            offsets[ip] -= 1
        else:
            # Otherwise (offset < 3), increase it by 1.
            offsets[ip] += 1
        
        # 3. Jump: Calculate the new instruction pointer
        ip += jump_offset
        
        # 4. Increment the step counter
        steps += 1
        
    if steps >= MAX_STEPS:
        print("Warning: Max steps reached. Program did not halt naturally.")
        
    return steps

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting jump maze simulation (Part 2 - Conditional Offset) using data from: {os.path.abspath(input_file)}\n")
    
    final_steps = solve_jump_maze(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: TOTAL STEPS REQUIRED TO REACH THE EXIT (Conditional Offset):")
    print(f"SCORE: {final_steps}")
    print("="*50)