import os
import re
from typing import List

# --- Constants ---
# Initial sequence of programs (16 total: 0 to 15)
INITIAL_PROGRAMS = list("abcdefghijklmnop")

def parse_moves(filepath):
    """
    Reads the comma-separated sequence of dance moves from the file.
    """
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            # Read single line, remove whitespace, and split by comma
            content = f.read().strip()
            moves = [m.strip() for m in content.split(',') if m.strip()]
    except FileNotFoundError:
        print(f"Error: Dance move file not found at '{filepath}'")
        return []
    
    return moves

def perform_dance_move(programs: List[str], move: str) -> List[str]:
    """
    Applies a single dance move (sX, xA/B, or pA/B) to the list of programs.
    """
    N = len(programs)
    move_type = move[0]
    args = move[1:]
    
    if move_type == 's':
        # Spin: sX (X programs move from end to front)
        X = int(args)
        
        # Pythonic rotation: suffix moves to the front
        # Example: abcde, s3 -> cdeab (suffix length 3 moves to front)
        shift = X % N
        programs = programs[N - shift:] + programs[:N - shift]
        
    elif move_type == 'x':
        # Exchange: xA/B (swap programs at positions A and B)
        A_str, B_str = args.split('/')
        A = int(A_str)
        B = int(B_str)
        
        # Simple swap by index
        programs[A], programs[B] = programs[B], programs[A]
        
    elif move_type == 'p':
        # Partner: pA/B (swap programs named A and B)
        A, B = args.split('/')
        
        # Find indices of the named programs
        try:
            idx_A = programs.index(A)
            idx_B = programs.index(B)
            
            # Swap by index
            programs[idx_A], programs[idx_B] = programs[idx_B], programs[idx_A]
        except ValueError:
            # Should not happen with valid input
            pass 

    return programs

def solve_dance_puzzle(filepath):
    """
    Orchestrates the dance simulation and returns the final program order.
    """
    dance_moves = parse_moves(filepath)
    if not dance_moves:
        return "".join(INITIAL_PROGRAMS)
        
    current_programs = INITIAL_PROGRAMS[:] # Start with a fresh copy
    
    print(f"Initial Order: {''.join(current_programs)}")
    print(f"Total Moves: {len(dance_moves)}")

    # Execute all moves sequentially
    for move in dance_moves:
        current_programs = perform_dance_move(current_programs, move)
        
    final_order = "".join(current_programs)
    
    return final_order

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting dance simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_result = solve_dance_puzzle(input_file)
    
    print("\n" + "="*50)
    print("FINAL ORDER OF PROGRAMS AFTER THE DANCE:")
    print(f"SCORE: {final_result}")
    print("="*50)