import os
import re

def parse_program(filepath):
    """
    Reads the assembunny instructions from the file.
    Returns a list of instruction lists: [opcode, arg1, arg2 (optional)]
    """
    program = []
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Program file not found at '{filepath}'")
        return []
        
    for line in lines:
        # Parse args; try to convert to int if possible, else keep as string (register name)
        parts = line.split()
        opcode = parts[0]
        args = []
        for arg in parts[1:]:
            try:
                args.append(int(arg))
            except ValueError:
                args.append(arg)
        
        program.append([opcode] + args)
            
    return program

def get_value(x, registers):
    """
    Helper to get value of integer literal or register.
    """
    if isinstance(x, int):
        return x
    return registers.get(x, 0)

def toggle_instruction(program, target_idx):
    """
    Modifies the instruction at target_idx based on TGL rules.
    """
    if not (0 <= target_idx < len(program)):
        return # Target outside program, nothing happens

    inst = program[target_idx]
    opcode = inst[0]
    args = inst[1:]
    
    # Logic for toggling
    if len(args) == 1:
        # One-argument instructions: inc <-> dec/tgl/etc
        if opcode == 'inc':
            inst[0] = 'dec'
        else:
            # dec, tgl -> inc
            inst[0] = 'inc'
            
    elif len(args) == 2:
        # Two-argument instructions: jnz <-> cpy
        if opcode == 'jnz':
            inst[0] = 'cpy'
        else:
            # cpy -> jnz
            inst[0] = 'jnz'

def run_vm(program, initial_registers=None):
    """
    Simulates the execution of the assembunny program with TGL support.
    """
    # Ensure the registers dictionary is mutable and correctly initialized
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    if initial_registers:
        registers.update(initial_registers)
        
    # We must operate on a COPY of the program list because TGL modifies it
    program_copy = [inst[:] for inst in program]

    ip = 0
    program_len = len(program_copy)
    
    # Increased step limit significantly for factorial-like complexity
    MAX_STEPS = 1000000000 
    step_count = 0

    while 0 <= ip < program_len and step_count < MAX_STEPS:
        
        # --- OPTIMIZATION: Detect Multiplication Loops ---
        # Structure: inc target, dec source, jnz source -2
        if ip + 2 < program_len:
            i0, i1, i2 = program_copy[ip], program_copy[ip+1], program_copy[ip+2]
            
            # Check for pattern integrity and required jump
            if i0[0] == 'inc' and i1[0] == 'dec' and i2[0] == 'jnz':
                if i2[1] == i1[1] and i2[2] == -2:
                    # Found addition loop: target += source; source = 0
                    target_reg = i0[1]
                    source_reg = i1[1]
                    
                    if isinstance(target_reg, str) and isinstance(source_reg, str):
                        registers[target_reg] += registers[source_reg]
                        registers[source_reg] = 0
                        ip += 3
                        step_count += 1
                        continue # Skip standard execution

        # --- STANDARD EXECUTION ---
        
        instruction = program_copy[ip]
        opcode = instruction[0]
        
        ip_increment = 1
        
        if opcode == 'cpy':
            # cpy x y: copies x into register y
            if len(instruction) == 3:
                x, y = instruction[1], instruction[2]
                # Skip if y is not a valid register (e.g., cpy 1 2)
                if isinstance(y, str):
                    val = get_value(x, registers)
                    registers[y] = val
            # else: skip invalid (malformed or toggled to invalid state)
                
        elif opcode == 'inc':
            # inc x: increments the value of register x
            if len(instruction) == 2:
                r = instruction[1]
                if isinstance(r, str):
                    registers[r] += 1
            
        elif opcode == 'dec':
            # dec x: decreases the value of register x
            if len(instruction) == 2:
                r = instruction[1]
                if isinstance(r, str):
                    registers[r] -= 1
            
        elif opcode == 'jnz':
            # jnz x y: jumps if x is not zero
            if len(instruction) == 3:
                x, y = instruction[1], instruction[2]
                val_x = get_value(x, registers)
                val_y = get_value(y, registers)
                
                if val_x != 0:
                    ip_increment = val_y
                
        elif opcode == 'tgl':
            # tgl x: toggles instruction x away
            if len(instruction) == 2:
                x = instruction[1]
                offset = get_value(x, registers)
                target_idx = ip + offset
                toggle_instruction(program_copy, target_idx)
            
        else:
            # Skip invalid opcode (e.g., cpy 1 2 when executed, or unknown opcode)
            pass

        # Update IP
        ip += ip_increment
        step_count += 1

    if step_count >= MAX_STEPS:
        print("Warning: Max steps reached. Program terminated early.")

    return registers

def solve_assembunny_puzzle(filepath, initial_a=7):
    """
    Loads the program and runs the simulation.
    """
    program = parse_program(filepath)
    if not program:
        return 0
    
    print(f"Program loaded: {len(program)} instructions.")
    
    # Set initial state
    initial_registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    
    final_registers = run_vm(program, initial_registers=initial_registers)
    
    print("-" * 50)
    print(f"Program Halted.")
    print(f"Final Registers: {final_registers}")
    
    return final_registers['a']

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    # Part 1: Inputs 'eggs' = 7
    START_A = 7
    
    print(f"Starting Assembunny simulation (Input A={START_A}) using data from: {os.path.abspath(input_file)}\n")
    
    final_a_value = solve_assembunny_puzzle(input_file, initial_a=START_A)
    
    print("\n" + "="*50)
    print("FINAL VALUE IN REGISTER 'a':")
    print(f"SCORE: {final_a_value}")
    print("="*50)