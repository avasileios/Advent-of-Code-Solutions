import os

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

    # Parse instruction pointer binding
    ip_reg = int(lines[0].split()[1])
    instructions = []
    for line in lines[1:]:
        parts = line.split()
        instructions.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))

    ops = get_ops()
    registers = [0] * 6
    ip = 0

    while 0 <= ip < len(instructions):
        # Write IP to the bound register
        registers[ip_reg] = ip
        
        # Fetch and execute
        op_name, a, b, c = instructions[ip]
        registers[c] = ops[op_name](registers, a, b)
        
        # Write bound register back to IP
        ip = registers[ip_reg]
        
        # Increment IP
        ip += 1

    return registers[0]

if __name__ == "__main__":
    print(f"Final value in register 0: {solve()}")