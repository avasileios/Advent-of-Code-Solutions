import os
import re

# Maximum 16-bit value (2^16 - 1)
MAX_16BIT = 65535 

def parse_instructions(filepath):
    """
    Reads instructions from the file and stores them in a map 
    where key=output_wire and value=instruction_list.
    """
    instructions = {}
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return {}
    
    # Regex to parse instruction: INPUT(s) -> OUTPUT
    for line in lines:
        parts = line.split(' -> ')
        if len(parts) == 2:
            output_wire = parts[1].strip()
            input_op = parts[0].strip().split()
            instructions[output_wire] = input_op
            
    return instructions

def solve_circuit(instructions, target_wire):
    """
    Finds the signal for the target wire using memoized recursion.
    
    Args:
        instructions (dict): Map of {output_wire: [instruction parts]}
        target_wire (str): The wire whose signal we are trying to find (e.g., 'a').
        
    Returns:
        int: The final signal value on the target wire.
    """
    # Memoization cache: stores {wire: signal}
    signals = {}
    
    def resolve(wire):
        """
        Recursively determines the signal value for a given wire.
        """
        # 1. Base Case: If the signal is already calculated, return it.
        if wire in signals:
            return signals[wire]
        
        # 2. Base Case: If the wire is a literal number, return it.
        try:
            return int(wire)
        except ValueError:
            pass # Not a number, proceed to find instruction
        
        # 3. Instruction Execution: Get the operation for the wire.
        op = instructions[wire]
        result = 0
        
        # --- Single Input Operations ---
        if len(op) == 1:
            # e.g., 123 -> x, or a -> x
            result = resolve(op[0])

        # --- NOT Operation ---
        elif len(op) == 2 and op[0] == 'NOT':
            # Bitwise complement, masked to 16 bits
            val = resolve(op[1])
            # ~val gives Python's large complement, so we mask it to 16-bit range
            # Formula: ~val & 0xFFFF 
            result = ~val & MAX_16BIT

        # --- Two Input Operations (AND, OR, LSHIFT, RSHIFT) ---
        elif len(op) == 3:
            wire1, gate, wire2 = op
            val1 = resolve(wire1)
            val2 = resolve(wire2)
            
            if gate == 'AND':
                result = val1 & val2
            elif gate == 'OR':
                result = val1 | val2
            elif gate == 'LSHIFT':
                # Left shift: needs to be masked to keep it 16-bit compliant
                result = (val1 << val2) & MAX_16BIT
            elif gate == 'RSHIFT':
                # Right shift (Python's >> handles this correctly)
                result = val1 >> val2
        
        # 4. Memoize and return
        signals[wire] = result
        return result

    # Start resolving the target wire
    final_signal = resolve(target_wire)
    
    return final_signal

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    TARGET_WIRE = 'a' # The wire whose signal we must find

    print(f"Starting circuit analysis for wire '{TARGET_WIRE}' using instructions from: {os.path.abspath(input_file)}\n")
    
    instructions = parse_instructions(input_file)
    
    if not instructions:
        exit()

    final_signal = solve_circuit(instructions, TARGET_WIRE)
    
    print("\n" + "="*50)
    print(f"SIGNAL ULTIMATELY PROVIDED TO WIRE '{TARGET_WIRE}':")
    print(f"SCORE: {final_signal}")
    print("="*50)