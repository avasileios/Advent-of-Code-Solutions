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

def get_sum_of_divisors(n):
    """Efficiently find the sum of all divisors of N."""
    divs = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n // i)
    return sum(divs)

def solve_part2():
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
    # Register 0 starts at 1 for Part 2
    registers = [1, 0, 0, 0, 0, 0]
    ip = 0

    # Step 1: Run for a few cycles to let the program initialize the large number
    # Usually, the target number is the largest value in the registers after 
    # the setup phase (around IP 33).
    for _ in range(1000):
        if not (0 <= ip < len(instructions)):
            break
        registers[ip_reg] = ip
        op_name, a, b, c = instructions[ip]
        registers[c] = ops[op_name](registers, a, b)
        ip = registers[ip_reg] + 1

    # The target number N is always the largest value in the registers
    # once the initialization loop finishes.
    target_n = max(registers)
    
    print(f"Detected target number N: {target_n}")
    
    # Step 2: Calculate sum of divisors mathematically
    result = get_sum_of_divisors(target_n)
    return result

if __name__ == "__main__":
    print(f"Final value in register 0 (Part 2): {solve_part2()}")