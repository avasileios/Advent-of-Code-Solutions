import os
import sys


def run_program(program):
    mem = program[:]
    pc = 0
    while True:
        op = mem[pc]
        if op == 1:
            mem[mem[pc + 3]] = mem[mem[pc + 1]] + mem[mem[pc + 2]]
            pc += 4
        elif op == 2:
            mem[mem[pc + 3]] = mem[mem[pc + 1]] * mem[mem[pc + 2]]
            pc += 4
        elif op == 99:
            return mem
        else:
            raise ValueError(f"bad opcode {op}")


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        program = [int(x) for x in f.read().strip().split(',')]

    for noun in range(100):
        for verb in range(100):
            p = program[:]
            p[1] = noun
            p[2] = verb
            if run_program(p)[0] == 19690720:
                print(100 * noun + verb)
                return


if __name__ == "__main__":
    main()
