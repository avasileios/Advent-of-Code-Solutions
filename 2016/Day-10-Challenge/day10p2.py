import os
from collections import defaultdict

# --- Target Constants ---
TARGET_LOW = 17
TARGET_HIGH = 61
OUTPUTS_TO_CHECK = [0, 1, 2]
# ------------------------

def parse_instructions(filepath):
    """
    Reads and separates instructions into initial values and bot logic rules.
    
    Returns:
        tuple: (initial_values: list of (value, bot_id), bot_rules: dict)
    """
    initial_values = []
    bot_rules = {}
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return None, None
        
    for line in lines:
        parts = line.split()
        
        if parts[0] == 'value':
            # Format: value 5 goes to bot 2
            value = int(parts[1])
            bot_id = int(parts[5])
            initial_values.append((value, bot_id))
            
        elif parts[0] == 'bot':
            # Format: bot 2 gives low to bot 1 and high to bot 0
            bot_id = int(parts[1])
            low_type = parts[5]    # 'bot' or 'output'
            low_id = int(parts[6])
            high_type = parts[10]  # 'bot' or 'output'
            high_id = int(parts[11])
            
            bot_rules[bot_id] = {
                'low_type': low_type, 
                'low_id': low_id, 
                'high_type': high_type, 
                'high_id': high_id
            }
            
    return initial_values, bot_rules

def solve_factory_puzzle(filepath):
    """
    Simulates the robot factory process. 
    Finds the Part 1 bot and calculates the Part 2 product.
    """
    initial_values, bot_rules = parse_instructions(filepath)
    if initial_values is None:
        return 0, 0

    # State containers
    bot_chips = defaultdict(list)
    outputs = defaultdict(list)
    
    # 1. Initialize bots with starting values
    for value, bot_id in initial_values:
        bot_chips[bot_id].append(value)
    
    winning_bot_id_p1 = None
    
    # 2. Simulation Loop
    while True:
        # Find all bots ready to execute (have exactly 2 chips)
        ready_bots = [bot_id for bot_id, chips in bot_chips.items() if len(chips) == 2]
        
        if not ready_bots:
            # System stabilized/halted.
            break

        # Process each ready bot
        for bot_id in ready_bots:
            chips = bot_chips[bot_id]
            chips.sort() # Sort the chips to determine low and high values
            
            low_value = chips[0]
            high_value = chips[1]
            
            # --- Check the Target Comparison (Part 1 Goal) ---
            if winning_bot_id_p1 is None and low_value == TARGET_LOW and high_value == TARGET_HIGH:
                winning_bot_id_p1 = bot_id
                
            # --- Execute Instruction ---
            if bot_id not in bot_rules:
                bot_chips[bot_id] = []
                continue

            rules = bot_rules[bot_id]

            # Clear the bot's chips (must happen before transfer)
            bot_chips[bot_id] = []

            # Low chip transfer
            if rules['low_type'] == 'bot':
                bot_chips[rules['low_id']].append(low_value)
            elif rules['low_type'] == 'output':
                outputs[rules['low_id']].append(low_value)
                
            # High chip transfer
            if rules['high_type'] == 'bot':
                bot_chips[rules['high_id']].append(high_value)
            elif rules['high_type'] == 'output':
                outputs[rules['high_id']].append(high_value)

    # --- Part 2 Calculation: Product of chips in outputs 0, 1, and 2 ---
    
    product = 1
    
    for output_id in OUTPUTS_TO_CHECK:
        if output_id in outputs and outputs[output_id]:
            # Use the value of ONE chip (the first one)
            product *= outputs[output_id][0]
        else:
            # If an output is missing, multiplication result is undefined (or 0 if required).
            # Assuming the inputs guarantee a chip ends up in 0, 1, and 2.
            print(f"Warning: Output bin {output_id} is empty or missing.")
            # For robustness, we return 0 if any required output is empty, although usually 
            # the simulation ensures all key outputs are filled.
            return winning_bot_id_p1, 0 
            
    return winning_bot_id_p1, product

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting robot factory simulation for Part 2 (Outputs) using data from: {os.path.abspath(input_file)}\n")
    
    winning_bot_id, final_product = solve_factory_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART 1: BOT RESPONSIBLE FOR COMPARING 61 WITH 17:")
    print(f"SCORE: {winning_bot_id}")
    print("-" * 50)
    print("PART 2: PRODUCT OF THE FIRST CHIP IN OUTPUTS 0, 1, AND 2:")
    print(f"SCORE: {final_product}")
    print("="*50)