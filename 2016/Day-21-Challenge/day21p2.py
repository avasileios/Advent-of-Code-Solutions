import os
import re

# --- Constants ---
INITIAL_PASSWORD = "abcdefgh"
SCRAMBLED_PASSWORD = "fbgdceah"
N = len(INITIAL_PASSWORD) # Length is 8

# CRITICAL FIX for Part 2: The correct reverse shift lookup table for N=8.
# Key (I_new): Index of letter X AFTER scrambling. 
# Value (L): Left shift needed to reverse the operation.
# I_new: [0, 1, 2, 3, 4, 5, 6, 7]
# L:     [1, 1, 6, 2, 7, 3, 0, 4]
REVERSE_ROTATE_AMOUNT = [1, 1, 6, 2, 7, 3, 0, 4]


def rotate_string(s: list, direction: str, steps: int) -> list:
    """
    Rotates the string (represented as a list of chars) left or right.
    """
    N = len(s)
    effective_steps = steps % N
    
    if direction == 'left':
        return s[effective_steps:] + s[:effective_steps]
    
    elif direction == 'right':
        return s[N - effective_steps:] + s[:N - effective_steps]
        
    return s

def execute_scrambling(password_list: list, instructions: list) -> list:
    """
    Executes the series of scrambling operations on the password list (Part 1).
    (Logic preserved from Part 1)
    """
    current_password = password_list
    
    for instruction in instructions:
        parts = instruction.split()
        op = parts[0] + parts[1]

        # --- SWAP Operations ---
        if op == 'swapposition':
            X = int(parts[2])
            Y = int(parts[5])
            current_password[X], current_password[Y] = current_password[Y], current_password[X]
            
        elif op == 'swapletter':
            X = parts[2]
            Y = parts[5]
            idx_X = current_password.index(X)
            idx_Y = current_password.index(Y)
            current_password[idx_X], current_password[idx_Y] = current_password[idx_Y], current_password[idx_X]
            
        # --- ROTATE Operations ---
        elif op == 'rotateleft':
            steps = int(parts[2])
            current_password = rotate_string(current_password, 'left', steps)
            
        elif op == 'rotateright':
            steps = int(parts[2])
            current_password = rotate_string(current_password, 'right', steps)
            
        elif op == 'rotatebased':
            X = parts[6]
            index = current_password.index(X)
            rotation_steps = 1 + index
            if index >= 4: rotation_steps += 1
            current_password = rotate_string(current_password, 'right', rotation_steps)
            
        # --- REVERSE Operation ---
        elif op == 'reversepositions':
            X = int(parts[2])
            Y = int(parts[4])
            sub_array = current_password[X : Y + 1]
            sub_array.reverse()
            current_password[X : Y + 1] = sub_array
            
        # --- MOVE Operation ---
        elif op == 'moveposition':
            X = int(parts[2])
            Y = int(parts[5])
            char_to_move = current_password.pop(X)
            current_password.insert(Y, char_to_move)
            
    return current_password


def execute_unscrambling(password_list: list, instructions: list) -> list:
    """
    Executes the series of scrambling operations in reverse order, applying 
    the inverse operation at each step (Part 2).
    """
    current_password = password_list
    N = len(current_password)
    
    # Reverse the order of instructions
    instructions.reverse()
    
    # We rely on this lookup table for the inverse shift amount L:
    REVERSE_ROTATE_AMOUNT = [1, 1, 6, 2, 7, 3, 0, 4]

    for instruction in instructions:
        parts = instruction.split()
        op = parts[0] + parts[1]
        
        # --- SWAP Operations (Self-inverting) ---
        if op == 'swapposition':
            X = int(parts[2])
            Y = int(parts[5])
            current_password[X], current_password[Y] = current_password[Y], current_password[X]
            
        elif op == 'swapletter':
            X = parts[2]
            Y = parts[5]
            idx_X = current_password.index(X)
            idx_Y = current_password.index(Y)
            current_password[idx_X], current_password[idx_Y] = current_password[idx_Y], current_password[idx_X]
            
        # --- ROTATE Operations (Reverse Direction) ---
        elif op == 'rotateleft':
            # Reverse: rotate right X steps
            steps = int(parts[2])
            current_password = rotate_string(current_password, 'right', steps)
            
        elif op == 'rotateright':
            # Reverse: rotate left X steps
            steps = int(parts[2])
            current_password = rotate_string(current_password, 'left', steps)
            
        elif op == 'rotatebased':
            # Reverse: rotate left by calculated inverse amount
            X = parts[6]
            # Find the new index I_new (where the letter X IS NOW)
            I_new = current_password.index(X)
            
            # The left rotation needed to reverse the operation is predetermined by I_new
            left_shift_amount = REVERSE_ROTATE_AMOUNT[I_new]
            
            # Apply the calculated LEFT rotation
            current_password = rotate_string(current_password, 'left', left_shift_amount)
            
        # --- REVERSE Operation (Self-inverting) ---
        elif op == 'reversepositions':
            # reverse positions X through Y
            X = int(parts[2])
            Y = int(parts[4])
            sub_array = current_password[X : Y + 1]
            sub_array.reverse()
            current_password[X : Y + 1] = sub_array
            
        # --- MOVE Operation (Reverse Arguments) ---
        elif op == 'moveposition':
            # Original: move X to Y. Reverse: move Y to X
            Y = int(parts[5]) # Original destination (now the source)
            X = int(parts[2]) # Original source (now the destination)
            
            # 1. Remove the character at Y
            char_to_move = current_password.pop(Y)
            
            # 2. Insert it at X
            current_password.insert(X, char_to_move)
            
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
    Loads instructions and executes the unscrambling simulation.
    """
    instructions = parse_input(filepath)
    if not instructions:
        return ""
        
    # Start with the scrambled password as a mutable list
    password_list = list(SCRAMBLED_PASSWORD)
    
    print(f"Starting Unscrambling from: {SCRAMBLED_PASSWORD}")
    print(f"Total Instructions: {len(instructions)}")

    # Execute all operations in reverse order
    final_password_list = execute_unscrambling(password_list, instructions)
    
    return "".join(final_password_list)

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting password unscrambler simulation (Part 2) using data from: {os.path.abspath(input_file)}\n")
    
    final_password = solve_scrambler_puzzle(input_file)
    
    print("\n" + "="*50)
    print("UN-SCRAMBLED VERSION OF THE PASSWORD:")
    print(f"SCORE: {final_password}")
    print("="*50)