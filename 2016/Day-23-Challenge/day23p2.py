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
    """Helper to get value of integer literal or register."""
    if isinstance(x, int):
        return x
    return registers.get(x, 0)

def toggle_instruction(program, target_idx):
    """Modifies the instruction at target_idx based on TGL rules."""
    if not (0 <= target_idx < len(program)):
        return

    inst = program[target_idx]
    opcode = inst[0]
    args = inst[1:]
    
    if len(args) == 1:
        if opcode == 'inc':
            inst[0] = 'dec'
        else:
            inst[0] = 'inc'
    elif len(args) == 2:
        if opcode == 'jnz':
            inst[0] = 'cpy'
        else:
            inst[0] = 'jnz'

def run_vm(program, initial_registers=None):
    """Simulates the execution of the assembunny program."""
    registers = initial_registers if initial_registers else {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    # Operate on a copy of the program list because TGL modifies it
    program_copy = [inst[:] for inst in program]
    ip = 0
    program_len = len(program_copy)
    
    MAX_STEPS = 100_000_000_000 # High limit for Part 2
    step_count = 0

    while 0 <= ip < program_len and step_count < MAX_STEPS:
        
        # --- OPTIMIZATION: Detect Multiplication Loops ---
        # Pattern for a += b * d:
        # cpy b c   (ip)
        # inc a     (ip+1)
        # dec c     (ip+2)
        # jnz c -2  (ip+3)
        # dec d     (ip+4)
        # jnz d -5  (ip+5)
        
        if ip + 5 < program_len:
            i0 = program_copy[ip]
            i1 = program_copy[ip+1]
            i2 = program_copy[ip+2]
            i3 = program_copy[ip+3]
            i4 = program_copy[ip+4]
            i5 = program_copy[ip+5]
            
            # Check for Multiplication Structure
            if (i0[0] == 'cpy' and i1[0] == 'inc' and i2[0] == 'dec' and 
                i3[0] == 'jnz' and i4[0] == 'dec' and i5[0] == 'jnz'):
                
                # Check Jumps
                if i3[2] == -2 and i5[2] == -5:
                    # Check register flow: cpy b c -> dec c -> jnz c
                    src_val_reg = i0[1] # b
                    temp_reg    = i0[2] # c
                    target_reg  = i1[1] # a
                    outer_loop_reg = i4[1] # d
                    
                    # Verify registers match the logic flow
                    if (i2[1] == temp_reg and i3[1] == temp_reg and 
                        i5[1] == outer_loop_reg):
                        
                        val_b = get_value(src_val_reg, registers)
                        val_d = get_value(outer_loop_reg, registers)
                        
                        # Perform Multiplication
                        registers[target_reg] += val_b * val_d
                        
                        # Reset counter registers
                        registers[temp_reg] = 0
                        registers[outer_loop_reg] = 0
                        
                        ip += 6
                        step_count += 1
                        continue

        # --- STANDARD EXECUTION ---
        instruction = program_copy[ip]
        opcode = instruction[0]
        ip_increment = 1
        
        if opcode == 'cpy':
            if len(instruction) == 3:
                x, y = instruction[1], instruction[2]
                if isinstance(y, str):
                    registers[y] = get_value(x, registers)
                
        elif opcode == 'inc':
            if len(instruction) == 2 and isinstance(instruction[1], str):
                registers[instruction[1]] += 1
            
        elif opcode == 'dec':
            if len(instruction) == 2 and isinstance(instruction[1], str):
                registers[instruction[1]] -= 1
            
        elif opcode == 'jnz':
            if len(instruction) == 3:
                x, y = instruction[1], instruction[2]
                val_x = get_value(x, registers)
                val_y = get_value(y, registers)
                if val_x != 0:
                    ip_increment = val_y
                
        elif opcode == 'tgl':
            if len(instruction) == 2:
                x = instruction[1]
                offset = get_value(x, registers)
                toggle_instruction(program_copy, ip + offset)

        ip += ip_increment
        step_count += 1

    if step_count >= MAX_STEPS:
        print("Warning: Max steps reached.")

    return registers

def solve_assembunny_puzzle(filepath, initial_a):
    program = parse_program(filepath)
    if not program: return 0
    
    print(f"Program loaded: {len(program)} instructions. Initial A={initial_a}")
    initial_registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    
    final_registers = run_vm(program, initial_registers=initial_registers)
    return final_registers['a']

# --- Main Execution Block ---
if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    # Part 2: Inputs 'eggs' = 12
    START_A = 12
    
    print(f"Starting Assembunny simulation (Input A={START_A}) using data from: {os.path.abspath(input_file)}\n")
    final_a_value = solve_assembunny_puzzle(input_file, initial_a=START_A)
    
    print("\n" + "="*50)
    print(f"FINAL VALUE IN REGISTER 'a' (Input A={START_A}):")
    print(f"SCORE: {final_a_value}")
    print("="*50)