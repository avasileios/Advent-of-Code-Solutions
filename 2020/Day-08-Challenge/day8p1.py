import os
import sys


def run(program):
    acc = 0
    pc = 0
    seen = set()
    while pc < len(program):
        if pc in seen:
            return acc, False
        seen.add(pc)
        op, arg = program[pc]
        if op == 'acc':
            acc += arg
            pc += 1
        elif op == 'jmp':
            pc += arg
        else:
            pc += 1
    return acc, True


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    program = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            op, arg = line.split(' ')
            program.append((op, int(arg)))

    acc, _ = run(program)
    print(acc)


if __name__ == "__main__":
    main()
