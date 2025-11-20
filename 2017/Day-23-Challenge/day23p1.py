import os
from collections import defaultdict
from typing import List, Dict, Any

# Initial registers start at 0
REGISTER_NAMES = "abcdefgh" 

def parse_program(filepath) -> List[List[Any]]:
    """
    Reads the coprocessor assembly instructions from the file.
    Returns a list of instruction lists: [opcode, arg1, arg2 (optional)]
    """
    program = []
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split()
                    
                    # Convert arguments to integer literals if possible
                    processed_args = []
                    for arg in parts[1:]:
                        try:
                            processed_args.append(int(arg))
                        except ValueError:
                            processed_args.append(arg)
                            
                    program.append([parts[0]] + processed_args)
    except FileNotFoundError:
        print(f"Error: Program file not found at '{filepath}'")
        return []
    return program

def get_value(x: Any, regs: defaultdict) -> int:
    """
    Helper to get value of register or integer literal.
    """
    if isinstance(x, int):
        return x
    return regs[x] # Register value (defaults to 0)

def run_vm(program):
    """
    Simulates the coprocessor program and counts the number of 'mul' instructions executed.
    """
    # Registers a-h start at 0
    regs = defaultdict(int)
    ip = 0 # Instruction Pointer
    program_len = len(program)
    mul_count = 0
    
    # Safety limit for maximum steps (The program often has long loops)
    MAX_STEPS = 100000000 
    step_count = 0

    while 0 <= ip < program_len and step_count < MAX_STEPS:
        step_count += 1
        
        cmd = program[ip]
        opcode = cmd[0]
        
        # Default IP increment is +1
        ip_increment = 1 
        
        # --- Instruction Execution ---
        
        if opcode == 'set':
            # set X Y: sets register X to the value of Y.
            Y_val = get_value(cmd[2], regs)
            regs[cmd[1]] = Y_val
            
        elif opcode == 'sub':
            # sub X Y: decreases register X by the value of Y.
            Y_val = get_value(cmd[2], regs)
            regs[cmd[1]] -= Y_val
            
        elif opcode == 'mul':
            # mul X Y: sets register X to the result of multiplying X by Y.
            Y_val = get_value(cmd[2], regs)
            regs[cmd[1]] *= Y_val
            
            # CRITICAL: Count the invocation
            mul_count += 1
            
        elif opcode == 'jnz':
            # jnz X Y: jumps with an offset of Y, but only if X is not zero.
            X_val = get_value(cmd[1], regs)
            Y_val = get_value(cmd[2], regs)
            
            if X_val != 0:
                ip_increment = Y_val
                
        # Update IP
        ip += ip_increment
        
    if step_count >= MAX_STEPS:
        print("Warning: Max steps reached. Program terminated early.")
        
    return mul_count

def solve_coprocessor_puzzle(filepath):
    """
    Loads the program and runs the simulation.
    """
    program = parse_program(filepath)
    if not program:
        return 0
        
    print(f"Program loaded: {len(program)} instructions.")
    
    final_mul_count = run_vm(program)
    
    return final_mul_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Coprocessor VM simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_coprocessor_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL TIMES THE 'mul' INSTRUCTION IS INVOKED:")
    print(f"SCORE: {final_count}")
    print("="*50)