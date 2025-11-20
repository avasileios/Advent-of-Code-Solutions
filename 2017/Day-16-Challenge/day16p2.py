import os
import re
from typing import List, Dict

# --- Constants ---
# Initial sequence of programs (16 total: 0 to 15)
INITIAL_PROGRAMS = list("abcdefghijklmnop")
TOTAL_DANCES = 1_000_000_000 # One billion

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
        shift = X % N
        programs = programs[N - shift:] + programs[:N - shift]
        
    elif move_type == 'x':
        # Exchange: xA/B (swap programs at positions A and B)
        A_str, B_str = args.split('/')
        A = int(A_str)
        B = int(B_str)
        programs[A], programs[B] = programs[B], programs[A]
        
    elif move_type == 'p':
        # Partner: pA/B (swap programs named A and B)
        A, B = args.split('/')
        
        try:
            idx_A = programs.index(A)
            idx_B = programs.index(B)
            programs[idx_A], programs[idx_B] = programs[idx_B], programs[idx_A]
        except ValueError:
            pass 

    return programs

def solve_dance_cycle(filepath):
    """
    Simulates the dance repeatedly to find the cycle length, then determines 
    the final order after 1 billion dances.
    """
    dance_moves = parse_moves(filepath)
    if not dance_moves:
        return "".join(INITIAL_PROGRAMS)
        
    # States map: {order_string: dance_number}
    # This detects when the order repeats.
    seen_states: Dict[str, int] = {} 
    
    # List to store the order at each step of the cycle for later lookup
    cycle_orders: List[str] = []
    
    current_programs = INITIAL_PROGRAMS[:] # Start with a fresh copy
    
    print(f"Initial Order: {''.join(current_programs)}")
    print(f"Total Dances to Simulate: {TOTAL_DANCES}")

    dance_number = 0
    
    # 1. Simulate until a cycle is detected
    while dance_number < TOTAL_DANCES:
        
        current_order = "".join(current_programs)
        
        if current_order in seen_states:
            # Cycle Detected!
            
            # The cycle starts at the dance number stored in seen_states[current_order]
            # but since we are interested in the cycle length back to the STARTING position,
            # we check if the state is equal to the initial state ('abcdefghijklmnop').
            
            # The total cycle length is dance_number (total steps taken).
            cycle_length = seen_states[current_order]
            print(f"\nCycle Detected! Order '{current_order}' first appeared at dance {cycle_length}.")
            print(f"Current dance number: {dance_number}")
            
            # 2. Calculate the remainder and final position
            
            # Effective dances needed after finding the cycle:
            remaining_dances = (TOTAL_DANCES - dance_number) % (dance_number - cycle_length)
            
            # The required order is stored at cycle_orders[cycle_length + remaining_dances]
            
            # Calculate the required index within the cycle_orders list
            # The order at dance_number is the first repetition. The order we want is 
            # (TOTAL_DANCES % cycle_length).
            
            # Index into cycle_orders for the result (0-indexed list)
            # cycle_orders[0] is the order AFTER dance 1.
            
            # Let's reset the cycle calculation for simplicity to the start:
            final_index = TOTAL_DANCES % dance_number
            
            # The result is the state achieved after final_index dances.
            return cycle_orders[final_index]


        # Record the state and the dance number *that achieved this state*
        seen_states[current_order] = dance_number
        cycle_orders.append(current_order)
        
        # Perform the dance
        for move in dance_moves:
            current_programs = perform_dance_move(current_programs, move)
            
        dance_number += 1
        
        if dance_number % 1000 == 0:
            print(f"Simulated {dance_number} dances...")

    # If TOTAL_DANCES was small enough (<= cycle_length), return the final order
    return "".join(current_programs)

# --- Main Execution Block ---
if __name__ == "__main__":
    input_file = "input.txt"
    print(f"Starting dance simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_result = solve_dance_cycle(input_file)
    
    print("\n" + "="*50)
    print("FINAL ORDER OF PROGRAMS AFTER ONE BILLION DANCES:")
    print(f"SCORE: {final_result}")
    print("="*50)