import os
import re

# --- Constants ---
INITIAL_PASSWORD = "abcdefgh"

def rotate_string(s: list, direction: str, steps: int) -> list:
    """
    Rotates the string (represented as a list of chars) left or right.
    """
    N = len(s)
    
    # Normalize steps to be within 0 and N-1
    effective_steps = steps % N
    
    if direction == 'left':
        # Rotate left: shift prefix to the end
        # Example: [1, 2, 3, 4], steps=1 -> [2, 3, 4, 1]
        return s[effective_steps:] + s[:effective_steps]
    
    elif direction == 'right':
        # Rotate right: shift suffix to the beginning
        # Example: [1, 2, 3, 4], steps=1 -> [4, 1, 2, 3]
        return s[N - effective_steps:] + s[:N - effective_steps]
        
    return s # Should not happen

def execute_scrambling(password_list: list, instructions: list) -> list:
    """
    Executes the series of scrambling operations on the password list.
    """
    current_password = password_list
    
    for instruction in instructions:
        parts = instruction.split()
        op = parts[0] + parts[1] # Combines first two words for opcode recognition
        
        # --- SWAP Operations ---
        if op == 'swapposition':
            # swap position X with position Y
            X = int(parts[2])
            Y = int(parts[5])
            current_password[X], current_password[Y] = current_password[Y], current_password[X]
            
        elif op == 'swapletter':
            # swap letter X with letter Y
            X = parts[2]
            Y = parts[5]
            
            # Find indices
            idx_X = current_password.index(X)
            idx_Y = current_password.index(Y)
            
            # Perform swap by position
            current_password[idx_X], current_password[idx_Y] = current_password[idx_Y], current_password[idx_X]
            
        # --- ROTATE Operations ---
        elif op == 'rotateleft':
            # rotate left X steps
            steps = int(parts[2])
            current_password = rotate_string(current_password, 'left', steps)
            
        elif op == 'rotateright':
            # rotate right X steps
            steps = int(parts[2])
            current_password = rotate_string(current_password, 'right', steps)
            
        elif op == 'rotatebased':
            # rotate based on position of letter X
            X = parts[6]
            index = current_password.index(X)
            
            # Base rotation: 1 step + index
            rotation_steps = 1 + index
            
            # Extra rotation if index >= 4
            if index >= 4:
                rotation_steps += 1
                
            # Apply rotation to the right
            current_password = rotate_string(current_password, 'right', rotation_steps)
            
        # --- REVERSE Operation ---
        elif op == 'reversepositions':
            # reverse positions X through Y
            X = int(parts[2])
            Y = int(parts[4])
            
            # Get the slice to reverse
            sub_array = current_password[X : Y + 1]
            sub_array.reverse()
            
            # Reinsert the reversed slice
            current_password[X : Y + 1] = sub_array
            
        # --- MOVE Operation ---
        elif op == 'moveposition':
            # move position X to position Y
            X = int(parts[2])
            Y = int(parts[5])
            
            # 1. Remove the character at X
            char_to_move = current_password.pop(X)
            
            # 2. Insert it at Y
            current_password.insert(Y, char_to_move)
            
    return current_password

def parse_input(filepath):
    """
    Reads the list of scrambling instructions.
    """
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return []

def solve_scrambler_puzzle(filepath):
    """
    Loads instructions and executes the scrambling simulation.
    """
    instructions = parse_input(filepath)
    if not instructions:
        return ""
        
    # Start with the initial password as a mutable list
    password_list = list(INITIAL_PASSWORD)
    
    print(f"Initial Password: {INITIAL_PASSWORD}")
    print(f"Total Instructions: {len(instructions)}")

    # Execute all operations in order
    final_password_list = execute_scrambling(password_list, instructions)
    
    return "".join(final_password_list)

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting password scrambler simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_password = solve_scrambler_puzzle(input_file)
    
    print("\n" + "="*50)
    print("RESULTING SCRAMBLED PASSWORD:")
    print(f"SCORE: {final_password}")
    print("="*50)