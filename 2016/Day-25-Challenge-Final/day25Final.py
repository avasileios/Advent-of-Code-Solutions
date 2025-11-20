import os

def parse_program(filepath):
    program = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip():
                    program.append(line.strip().split())
    except FileNotFoundError:
        print(f"Error: Input file not found at {filepath}")
        return []
    return program

def get_val(x, regs):
    try:
        return int(x)
    except ValueError:
        return regs[x]

def run_check(program, start_a):
    """
    Runs the program with register a = start_a.
    Returns True if it produces the clock signal 0, 1, 0, 1... for a sufficient length.
    Returns False otherwise.
    """
    regs = {'a': start_a, 'b': 0, 'c': 0, 'd': 0}
    ip = 0
    output_count = 0
    expected_bit = 0
    max_outputs = 50 # Sufficient to detect the repeating pattern
    
    # Safety limit for cycles without output
    steps = 0
    max_steps = 100000 

    while 0 <= ip < len(program):
        if output_count >= max_outputs:
            return True # Found it!

        if steps > max_steps:
            return False # Taking too long without output
        steps += 1

        cmd = program[ip]
        op = cmd[0]

        if op == 'cpy':
            x, y = cmd[1], cmd[2]
            if y in regs: # valid register
                regs[y] = get_val(x, regs)
            ip += 1
        elif op == 'inc':
            x = cmd[1]
            if x in regs:
                regs[x] += 1
            ip += 1
        elif op == 'dec':
            x = cmd[1]
            if x in regs:
                regs[x] -= 1
            ip += 1
        elif op == 'jnz':
            x, y = cmd[1], cmd[2]
            val_x = get_val(x, regs)
            val_y = get_val(y, regs)
            if val_x != 0:
                ip += val_y
            else:
                ip += 1
        elif op == 'out':
            x = cmd[1]
            val = get_val(x, regs)
            
            # Check clock signal integrity
            if val != expected_bit:
                return False # Pattern broken
            
            expected_bit = 1 - expected_bit # Toggle expectation (0->1, 1->0)
            output_count += 1
            steps = 0 # Reset step safety counter on successful output
            ip += 1
        else:
            ip += 1 # Skip unknown instructions (like tgl if it appeared here)

    return False

def solve_clock_puzzle(filepath):
    program = parse_program(filepath)
    if not program:
        return

    # Heuristic: The value is usually not massive, but we iterate until we find it.
    a = 0
    print("Searching for the lowest positive integer 'a'...")
    while True:
        if a % 100 == 0:
            # Simple progress indicator
            pass 
            
        if run_check(program, a):
            return a
        a += 1

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    # Ensure the path is correct relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, input_file)

    result = solve_clock_puzzle(full_path)
    
    print("\n" + "="*50)
    print("LOWEST POSITIVE INTEGER FOR REGISTER 'a':")
    print(f"SCORE: {result}")
    print("="*50)