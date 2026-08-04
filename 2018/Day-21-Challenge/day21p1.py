import os
import re

def get_ops():
    return {
        "addr": lambda r, a, b: r[a] + r[b],
        "addi": lambda r, a, b: r[a] + b,
        "mulr": lambda r, a, b: r[a] * r[b],
        "muli": lambda r, a, b: r[a] * b,
        "banr": lambda r, a, b: r[a] & r[b],
        "bani": lambda r, a, b: r[a] & b,
        "borr": lambda r, a, b: r[a] | r[b],
        "bori": lambda r, a, b: r[a] | b,
        "setr": lambda r, a, b: r[a],
        "seti": lambda r, a, b: a,
        "gtir": lambda r, a, b: 1 if a > r[b] else 0,
        "gtri": lambda r, a, b: 1 if r[a] > b else 0,
        "gtrr": lambda r, a, b: 1 if r[a] > r[b] else 0,
        "eqir": lambda r, a, b: 1 if a == r[b] else 0,
        "eqri": lambda r, a, b: 1 if r[a] == b else 0,
        "eqrr": lambda r, a, b: 1 if r[a] == r[b] else 0,
    }

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    with open(file_path, 'r') as f:
        lines = f.readlines()

    ip_reg = int(lines[0].split()[1])
    instructions = []
    for line in lines[1:]:
        parts = line.split()
        instructions.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))

    ops = get_ops()
    registers = [0, 0, 0, 0, 0, 0]
    ip = 0

    while 0 <= ip < len(instructions):
        op_name, a, b, c = instructions[ip]
        
        # MONITORING POINT:
        # Find the instruction that compares a register to Register 0.
        # In most inputs, this is 'eqrr X 0 Y' or 'eqrr 0 X Y'.
        if op_name == "eqrr":
            # The value being compared to Register 0 is the answer.
            # Usually it's register 'a' being compared to 'b' (where b is 0).
            target_val = registers[a] if b == 0 else registers[b]
            return target_val

        # Standard execution
        registers[ip_reg] = ip
        registers[c] = ops[op_name](registers, a, b)
        ip = registers[ip_reg] + 1

if __name__ == "__main__":
    print(f"The lowest value for Register 0 to halt earliest is: {solve()}")