import re
import os

def solve():
    # Setup path to find input.txt in the same directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')

    if not os.path.exists(file_path):
        print("Error: input.txt not found.")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    # The first section contains the samples. 
    # It is separated from the test program by four newlines.
    sections = content.split('\n\n\n')
    samples_raw = sections[0].strip().split('\n\n')

    # Define all 16 operations
    # A, B are inputs, C is output register, R is register state
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

    three_plus_matches = 0

    for sample in samples_raw:
        # Extract digits: 0-3 (Before), 4-7 (Instruction), 8-11 (After)
        nums = [int(n) for n in re.findall(r'\d+', sample)]
        if len(nums) < 12: continue # Safety check for trailing data
        
        before = nums[0:4]
        instr = nums[4:8]
        after = nums[8:12]
        
        _, a, b, c = instr
        matches = 0
        
        for name, func in ops.items():
            # Test if the operation produces the 'after' value in register C
            # while keeping other registers the same
            try:
                result_val = func(before, a, b)
                if result_val == after[c]:
                    # Also ensure the instruction didn't somehow change other registers
                    # (Though the rules say only C is written to)
                    matches += 1
            except (IndexError, KeyError):
                # Some inputs might point to non-existent registers
                continue
        
        if matches >= 3:
            three_plus_matches += 1

    print(f"Number of samples that behave like 3 or more opcodes: {three_plus_matches}")

if __name__ == "__main__":
    solve()