import os
import re
from collections import defaultdict

def parse_blueprint(filepath):
    """
    Parses the Turing machine blueprint file.
    
    Returns:
        start_state (str)
        checksum_steps (int)
        rules (dict): {state: {current_val: (write_val, move_dir, next_state)}}
    """
    rules = {}
    start_state = None
    checksum_steps = 0
    
    current_state = None
    current_val = None
    
    try:
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: Blueprint file not found at '{filepath}'")
        return None, 0, {}

    for line in lines:
        if not line:
            continue
            
        # Header Parsing
        if line.startswith("Begin in state"):
            start_state = line.split()[-1].rstrip('.')
        
        elif line.startswith("Perform a diagnostic checksum"):
            # Extract number of steps
            parts = line.split()
            # usually 6th word: "after X steps."
            for part in parts:
                if part.isdigit():
                    checksum_steps = int(part)
                    break
                    
        # State Parsing
        elif line.startswith("In state"):
            # Format: "In state A:"
            current_state = line.split()[-1].rstrip(':')
            rules[current_state] = {}
            
        elif line.startswith("If the current value is"):
            # Format: "If the current value is 0:"
            val_char = line.split()[-1].rstrip(':')
            current_val = int(val_char)
            
        elif line.startswith("- Write the value"):
            # Format: "- Write the value 1."
            write_val = int(line.split()[-1].rstrip('.'))
            # We temporarily store this until we get the other 2 parts
            # But since the structure is fixed, we can just build up a list or dict
            # Let's use a temporary holder on the rules dict for now? 
            # Actually, assuming strict order (Write, Move, Continue), we can just 
            # start a partial tuple.
            rules[current_state][current_val] = {'write': write_val}

        elif line.startswith("- Move one slot to the"):
            # Format: "- Move one slot to the right."
            direction_str = line.split()[-1].rstrip('.')
            move_dir = 1 if direction_str == 'right' else -1
            rules[current_state][current_val]['move'] = move_dir
            
        elif line.startswith("- Continue with state"):
            # Format: "- Continue with state B."
            next_state = line.split()[-1].rstrip('.')
            
            # Finalize the rule tuple for this state/val pair
            partial = rules[current_state][current_val]
            rules[current_state][current_val] = (partial['write'], partial['move'], next_state)

    return start_state, checksum_steps, rules

def run_turing_machine(start_state, steps, rules):
    """
    Simulates the Turing machine.
    Using a set to store positions of '1's for efficiency (Tape is infinite 0s).
    """
    # Tape stores indices where value is 1. All other indices are implicitly 0.
    ones_on_tape = set()
    
    cursor = 0
    state = start_state
    
    # Progress reporting interval
    report_interval = steps // 10 if steps > 0 else 1
    if report_interval == 0: report_interval = 1

    print(f"Simulating {steps} steps...")

    for step in range(1, steps + 1):
        # 1. Read
        current_val = 1 if cursor in ones_on_tape else 0
        
        # 2. Lookup Rule
        if state not in rules or current_val not in rules[state]:
            print(f"Error: No rule defined for State {state}, Value {current_val}")
            break
            
        write_val, move_dir, next_state = rules[state][current_val]
        
        # 3. Write
        if write_val == 1:
            ones_on_tape.add(cursor)
        else:
            ones_on_tape.discard(cursor) # Set to 0
            
        # 4. Move
        cursor += move_dir
        
        # 5. Transition
        state = next_state
        
        if step % report_interval == 0:
             # Optional progress bar
             pass

    return len(ones_on_tape)

def solve_turing_puzzle(filepath):
    start_state, steps, rules = parse_blueprint(filepath)
    
    if not rules:
        return 0
        
    print(f"Blueprint parsed. Start: {start_state}, Steps: {steps}")
    print(f"States found: {list(rules.keys())}")
    
    checksum = run_turing_machine(start_state, steps, rules)
    
    return checksum

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction
    input_file = "input.txt"
    
    print(f"Starting Turing Machine simulation using blueprint: {os.path.abspath(input_file)}\n")
    
    final_checksum = solve_turing_puzzle(input_file)
    
    print("\n" + "="*50)
    print("DIAGNOSTIC CHECKSUM (Number of 1s on tape):")
    print(f"SCORE: {final_checksum}")
    print("="*50)