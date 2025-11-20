import os
import re

def parse_program(filepath):
    """
    Reads the assembunny instructions from the file.
    
    Returns:
        list: A list of instruction lists, where each inner list is 
              [opcode, arg1, arg2 (optional)].
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
        program.append(line.split())
            
    return program

def get_value(x, registers):
    """
    Helper function to get the value of an argument, which can be an integer 
    literal or the value of a register.
    """
    try:
        return int(x)
    except ValueError:
        # It must be a register (a, b, c, or d)
        return registers.get(x, 0) # Use .get with default 0 for safety

def run_vm(program, initial_registers=None):
    """
    Simulates the execution of the assembunny program.
    
    Args:
        program (list): The parsed list of instructions.
        initial_registers (dict, optional): Starting values for registers a, b, c, d.
        
    Returns:
        dict: The final register values.
    """
    # Initialize registers a, b, c, d to 0, or use provided initial values
    # Ensure all required registers are present, defaulting to 0
    default_registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    if initial_registers:
        default_registers.update(initial_registers)
        
    registers = default_registers
    
    ip = 0 # Instruction Pointer
    program_len = len(program)
    
    # We use a high step limit to catch potential infinite loops
    # Increased MAX_STEPS for Part 2 complexity (since the program may compute factorials/large numbers)
    MAX_STEPS = 100000000 
    step_count = 0

    while 0 <= ip < program_len and step_count < MAX_STEPS:
        instruction = program[ip]
        opcode = instruction[0]
        
        # Default increment is +1, modified only by the jnz instruction
        ip_increment = 1 
        
        # --- EXECUTE INSTRUCTION ---
        
        if opcode == 'cpy':
            # cpy x y: copies x into register y
            x = instruction[1]
            y = instruction[2]
            
            value_to_copy = get_value(x, registers)
            registers[y] = value_to_copy
            
        elif opcode == 'inc':
            # inc x: increases the value of register x by one
            r = instruction[1]
            registers[r] += 1
            
        elif opcode == 'dec':
            # dec x: decreases the value of register x by one
            r = instruction[1]
            registers[r] -= 1
            
        elif opcode == 'jnz':
            # jnz x y: jumps to instruction y away if x is not zero
            x = instruction[1] # Check condition (register or literal)
            y = instruction[2] # Offset (literal)
            
            check_value = get_value(x, registers)
            offset = get_value(y, registers) # Offset is always a literal in P1, but read safely
            
            if check_value != 0:
                ip_increment = offset
                
        # Update IP
        ip += ip_increment
        step_count += 1
        
    if step_count >= MAX_STEPS:
        print("Warning: Max steps reached. Program may be in an infinite loop or performing an intensive calculation.")

    return registers

def solve_assembunny_puzzle(filepath, c_initial_value=0):
    """
    Loads the program and runs the simulation.
    """
    program = parse_program(filepath)
    if not program:
        return 0
        
    print(f"Program loaded: {len(program)} instructions.")
    
    # Set initial state
    initial_registers = {'a': 0, 'b': 0, 'c': c_initial_value, 'd': 0}
    
    # Run simulation
    final_registers = run_vm(program, initial_registers=initial_registers)
    
    print("-" * 50)
    print(f"Program Halted after processing.")
    print(f"Final Registers: {final_registers}")
    
    return final_registers['a']

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    # --- PART TWO EXECUTION: C initialized to 1 ---
    C_START = 1 
    
    print(f"Starting Assembunny simulation (Part Two: C={C_START}) using data from: {os.path.abspath(input_file)}\n")
    
    final_a_value = solve_assembunny_puzzle(input_file, c_initial_value=C_START)
    
    print("\n" + "="*50)
    print("FINAL VALUE IN REGISTER 'a' (Starting C=1):")
    print(f"SCORE: {final_a_value}")
    print("="*50)