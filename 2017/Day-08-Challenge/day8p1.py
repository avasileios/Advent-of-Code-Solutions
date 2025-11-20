import os
from collections import defaultdict
import operator
import re
from typing import Dict

# Map string operators to Python's operator functions
OP_MAP = {
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne
}

def evaluate_condition(registers: Dict[str, int], condition_parts: list) -> bool:
    """
    Evaluates the conditional statement (e.g., 'a > 1').
    
    Args:
        registers (dict): Current state of all registers.
        condition_parts (list): [reg_name, operator, value_str]
        
    Returns:
        bool: True if the condition is met, False otherwise.
    """
    
    # Condition structure: [reg_name, operator, value]
    reg_name, op_str, val_str = condition_parts
    
    # Get register value (defaults to 0 if not yet defined)
    reg_value = registers[reg_name] 
    
    # Get comparison value
    try:
        compare_value = int(val_str)
    except ValueError:
        # Should not happen with valid input, but safety first
        return False
        
    # Get the required operator function
    op_func = OP_MAP.get(op_str)
    
    if op_func:
        return op_func(reg_value, compare_value)
        
    return False

def solve_register_puzzle(filepath):
    """
    Simulates the instruction sequence and returns the largest value ever held in any register.
    """
    # Use defaultdict to initialize any new register to 0 automatically
    registers = defaultdict(int)
    max_value_in_any_register = 0 # Tracks the maximum value *at the end* of all instructions
    max_value_ever_seen = 0        # Tracks the maximum value ever seen in any register

    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            instructions = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return 0
    
    # The instruction lines are: target_reg op amount if cond_reg op_cond value
    # Example: b inc 5 if a > 1
    
    for line in instructions:
        # Split the line into two halves: Instruction and Condition
        try:
            instruction_str, condition_str = line.split(" if ")
        except ValueError:
            continue # Skip malformed lines

        # 1. Parse Instruction: [target_reg, op, amount]
        # Example: ['b', 'inc', '5']
        target_reg, operation, amount_str = instruction_str.split()
        amount = int(amount_str)
        
        # 2. Parse Condition: [cond_reg, op_cond, value]
        # Example: ['a', '>', '1']
        condition_parts = condition_str.split()

        # 3. Evaluate the Condition (Crucial step)
        if evaluate_condition(registers, condition_parts):
            
            # 4. Execute the Instruction
            
            # Get the current value (defaulting to 0 if new register)
            current_val = registers[target_reg]
            
            if operation == 'inc':
                new_val = current_val + amount
            elif operation == 'dec':
                # Decreasing by -10 means current_val - (-10) = current_val + 10
                new_val = current_val - amount
            else:
                # Skip unknown operations
                continue
                
            # Update register
            registers[target_reg] = new_val
            
            # 5. Update maximum value ever seen
            max_value_ever_seen = max(max_value_ever_seen, new_val)


    # After all instructions, find the largest value in the final state of all registers
    # We include max_value_ever_seen for Part 2 continuity, but for Part 1, we just need max(registers.values())
    if registers:
        max_value_in_any_register = max(registers.values())
    
    # Store both results (Part 1 and Part 2 use slightly different outputs)
    return max_value_in_any_register, max_value_ever_seen

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting conditional register simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_max, max_ever = solve_register_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART 1: LARGEST VALUE IN ANY REGISTER (Final State):")
    print(f"SCORE: {final_max}")
    print("="*50)