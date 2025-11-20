import os
import re

def parse_program(filepath):
    """
    Reads the assembly instructions from the file.
    
    Returns:
        list: A list of instruction lists, where each inner list is 
              [opcode, register/offset_val].
    """
    program = []
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Program file not found at '{filepath}'")
        return []
        
    # Regex to capture instructions like: hlf r, jio r, offset, jmp offset
    # It separates the opcode from the arguments.
    # Pattern groups: (opcode) (arg1) (comma + arg2)?
    pattern = re.compile(r'(\w+)\s+([a-z\+\-0-9]+)(?:,\s*([a-z\+\-0-9]+))?')

    for line in lines:
        match = pattern.match(line)
        if match:
            opcode = match.group(1)
            arg1 = match.group(2)
            arg2 = match.group(3)
            
            instruction = [opcode]
            instruction.append(arg1)
            if arg2:
                instruction.append(arg2)
            
            program.append(instruction)
            
    return program

def run_vm(program, initial_a=0, initial_b=0):
    """
    Simulates the execution of the assembly program.
    
    Args:
        program (list): The parsed list of instructions.
        initial_a (int): Starting value for register 'a'.
        initial_b (int): Starting value for register 'b'.
        
    Returns:
        dict: The final register values.
    """
    registers = {'a': initial_a, 'b': initial_b}
    ip = 0 # Instruction Pointer
    program_len = len(program)
    
    # We use a high step limit to catch infinite loops, though the program should halt naturally.
    MAX_STEPS = 10000000 
    step_count = 0

    while 0 <= ip < program_len and step_count < MAX_STEPS:
        instruction = program[ip]
        opcode = instruction[0]
        
        # Default increment is +1, modified only by jump instructions
        ip_increment = 1 
        
        # --- EXECUTE INSTRUCTION ---
        
        if opcode == 'hlf':
            r = instruction[1]
            registers[r] //= 2
            
        elif opcode == 'tpl':
            r = instruction[1]
            registers[r] *= 3
            
        elif opcode == 'inc':
            r = instruction[1]
            registers[r] += 1
            
        elif opcode == 'jmp':
            offset = int(instruction[1])
            ip_increment = offset
            
        elif opcode == 'jie':
            r = instruction[1]
            offset = int(instruction[2])
            
            # Jump if register r is even
            if registers[r] % 2 == 0:
                ip_increment = offset
            
        elif opcode == 'jio':
            r = instruction[1]
            offset = int(instruction[2])
            
            # Jump if register r is exactly 1
            if registers[r] == 1:
                ip_increment = offset
                
        else:
            print(f"Unknown opcode: {opcode} at IP={ip}")
            break

        # Update IP (the default +1 is implicitly handled by ip_increment)
        ip += ip_increment
        step_count += 1
        
    if step_count >= MAX_STEPS:
        print("Warning: Max steps reached. Program may be in an infinite loop.")

    return registers

def solve_assembly_puzzle(filepath):
    """
    Loads the program and runs the simulation starting with a=0, b=0.
    """
    program = parse_program(filepath)
    if not program:
        return 0
        
    print(f"Program loaded: {len(program)} instructions.")
    
    # Run simulation with initial state a=0, b=0
    final_registers = run_vm(program, initial_a=0, initial_b=0)
    
    print("-" * 50)
    print(f"Program Halted after processing.")
    
    return final_registers['b']

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting assembly simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_b_value = solve_assembly_puzzle(input_file)
    
    print("\n" + "="*50)
    print("FINAL VALUE IN REGISTER 'b':")
    print(f"SCORE: {final_b_value}")
    print("="*50)