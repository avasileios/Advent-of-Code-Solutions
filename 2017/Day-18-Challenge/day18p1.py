import os
from collections import defaultdict

# --- Constants ---
# Registers are named by single letters.
REGISTER_NAMES = "abcdefghijklmnopqrstuvwxyz" 

def parse_program(filepath):
    """
    Reads the Duet assembly instructions from the file.
    Returns a list of instruction lists: [opcode, arg1, arg2 (optional)]
    """
    program = []
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    program.append(line.strip().split())
    except FileNotFoundError:
        print(f"Error: Program file not found at '{filepath}'")
        return []
    return program

def get_value(x_str: str, regs: defaultdict) -> int:
    """
    Helper to get value of register or integer literal.
    """
    try:
        return int(x_str)
    except ValueError:
        return regs[x_str] # Defaults to 0 if register is new/uninitialized

def run_vm(program):
    """
    Simulates the Duet program until the first successful 'rcv' operation.
    
    Returns:
        int: The value of the recovered frequency (last sound played).
    """
    # Registers start at 0
    regs = defaultdict(int)
    ip = 0 # Instruction Pointer
    last_sound = 0
    program_len = len(program)
    
    # Safety limit for maximum steps
    MAX_STEPS = 10000000 
    step_count = 0

    while 0 <= ip < program_len and step_count < MAX_STEPS:
        step_count += 1
        
        cmd = program[ip]
        opcode = cmd[0]
        
        # Default IP increment is +1
        ip_increment = 1 
        
        # --- Instruction Execution ---
        
        if opcode == 'snd':
            # snd X: plays a sound with a frequency equal to the value of X.
            X_val = get_value(cmd[1], regs)
            last_sound = X_val
            
        elif opcode == 'set':
            # set X Y: sets register X to the value of Y.
            Y_val = get_value(cmd[2], regs)
            regs[cmd[1]] = Y_val
            
        elif opcode == 'add':
            # add X Y: increases register X by the value of Y.
            Y_val = get_value(cmd[2], regs)
            regs[cmd[1]] += Y_val
            
        elif opcode == 'mul':
            # mul X Y: sets register X to the result of multiplying X by Y.
            Y_val = get_value(cmd[2], regs)
            regs[cmd[1]] *= Y_val
            
        elif opcode == 'mod':
            # mod X Y: sets register X to the remainder of X modulo Y.
            Y_val = get_value(cmd[2], regs)
            # Ensure division by zero doesn't crash the simulation
            if Y_val != 0:
                regs[cmd[1]] %= Y_val
            
        elif opcode == 'rcv':
            # rcv X: recovers the frequency of the last sound played, 
            # but only when the value of X is not zero.
            X_val = get_value(cmd[1], regs)
            if X_val != 0:
                # SUCCESS: Recover operation executed with a non-zero value
                return last_sound
            
        elif opcode == 'jgz':
            # jgz X Y: jumps with an offset of Y, but only if X is greater than zero.
            X_val = get_value(cmd[1], regs)
            Y_val = get_value(cmd[2], regs)
            
            if X_val > 0:
                ip_increment = Y_val
                
        else:
            # Skip unknown instructions
            pass

        # Update IP
        ip += ip_increment
        
    if step_count >= MAX_STEPS:
        print("Warning: Max steps reached. Program terminated early.")
        
    return 0 # Program terminated before a successful recovery

def solve_duet_puzzle(filepath):
    """
    Loads the program and runs the simulation.
    """
    program = parse_program(filepath)
    if not program:
        return 0
        
    print(f"Program loaded: {len(program)} instructions.")
    
    final_recovered_frequency = run_vm(program)
    
    return final_recovered_frequency

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Duet VM simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_frequency = solve_duet_puzzle(input_file)
    
    print("\n" + "="*50)
    print("VALUE OF THE RECOVERED FREQUENCY:")
    print(f"SCORE: {final_frequency}")
    print("="*50)