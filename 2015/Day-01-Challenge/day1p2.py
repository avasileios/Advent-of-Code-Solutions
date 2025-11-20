import os

def solve_floor_puzzle(directions_file):
    """
    Calculates the final floor number (Part 1) and the position of the first 
    character that causes Santa to enter the basement (floor -1) (Part 2).
    """
    try:
        # Robust path reading
        with open(directions_file, 'r') as f:
            instructions = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{directions_file}'")
        return None, None
    
    if not instructions:
        return 0, 0
        
    current_floor = 0
    first_basement_position = None
    
    # Iterate through instructions to simulate movement and find the first basement entry
    for position, instruction in enumerate(instructions, 1):
        
        # 1. Update floor based on instruction
        if instruction == '(':
            current_floor += 1
        elif instruction == ')':
            current_floor -= 1
        
        # 2. Check for the first entry into the basement (floor -1)
        if current_floor == -1 and first_basement_position is None:
            first_basement_position = position
    
    # Part 1 Result: Final floor is the last calculated floor
    final_floor = current_floor
    
    # Part 2 Result: Position of the first character to reach floor -1
    return final_floor, first_basement_position

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting floor calculation using instructions from: {os.path.abspath(input_file)}\n")
    
    final_floor, first_basement_pos = solve_floor_puzzle(input_file)
    
    if final_floor is not None:
        # Display Part 1 Result
        print("\n" + "="*50)
        print("PART 1: FINAL FLOOR NUMBER:")
        print(f"SCORE: {final_floor}")
        print("-" * 50)
        
        # Display Part 2 Result
        print("PART 2: POSITION OF FIRST BASEMENT ENTRY (Floor -1):")
        if first_basement_pos is not None:
            print(f"SCORE: {first_basement_pos}")
        else:
            print("Santa never enters the basement (-1).")
        print("="*50)