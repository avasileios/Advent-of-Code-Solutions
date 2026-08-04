import re
import os

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')

    with open(file_path, 'r') as f:
        content = f.read()

    # Split into Samples and Program sections
    parts = content.split('\n\n\n')
    samples_raw = parts[0].strip().split('\n\n')
    program_raw = parts[1].strip().split('\n')

    # Define all opcodes
    ops = {
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

    # Step 1: Identify possible names for each opcode number
    possible_mappings = {i: set(ops.keys()) for i in range(16)}

    for sample in samples_raw:
        nums = [int(n) for n in re.findall(r'\d+', sample)]
        before, instr, after = nums[0:4], nums[4:8], nums[8:12]
        op_num, a, b, c = instr
        
        valid_for_this_sample = set()
        for name, func in ops.items():
            if func(before, a, b) == after[c]:
                valid_for_this_sample.add(name)
        
        # Intersection: only keep names that were valid for this sample
        possible_mappings[op_num] &= valid_for_this_sample

    # Step 2: Narrow down to unique mappings
    known_mapping = {}
    while len(known_mapping) < 16:
        for op_num, potentials in possible_mappings.items():
            if len(potentials) == 1:
                name = potentials.pop()
                known_mapping[op_num] = name
                # Remove this identified name from all other sets
                for other_num in possible_mappings:
                    possible_mappings[other_num].discard(name)

    # Step 3: Run the test program
    registers = [0, 0, 0, 0]
    for line in program_raw:
        if not line.strip(): continue
        op_num, a, b, c = [int(n) for n in re.findall(r'\d+', line)]
        op_name = known_mapping[op_num]
        registers[c] = ops[op_name](registers, a, b)

    print(f"Final value in register 0: {registers[0]}")

if __name__ == "__main__":
    solve()