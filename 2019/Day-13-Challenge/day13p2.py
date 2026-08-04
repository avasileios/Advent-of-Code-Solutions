import os
import sys


class Intcode:
    def __init__(self, program, inputs=None):
        self.mem = list(program) + [0] * 100000
        self.pc = 0
        self.rel = 0
        self.inputs = list(inputs or [])
        self.inp_idx = 0
        self.outputs = []
        self.halted = False

    def run(self, inputs=None):
        if inputs:
            self.inputs.extend(inputs)
        while not self.halted:
            op = self.mem[self.pc] % 100
            mode = self.mem[self.pc] // 100

            def get(p):
                m = (mode // 10 ** (p - 1)) % 10
                v = self.mem[self.pc + p]
                if m == 0:
                    return self.mem[v]
                if m == 1:
                    return v
                return self.mem[v + self.rel]

            def setp(p, val):
                m = (mode // 10 ** (p - 1)) % 10
                v = self.mem[self.pc + p]
                if m == 0:
                    self.mem[v] = val
                else:
                    self.mem[v + self.rel] = val

            if op == 1:
                setp(3, get(1) + get(2))
                self.pc += 4
            elif op == 2:
                setp(3, get(1) * get(2))
                self.pc += 4
            elif op == 3:
                if self.inp_idx >= len(self.inputs):
                    return self.outputs
                setp(1, self.inputs[self.inp_idx])
                self.inp_idx += 1
                self.pc += 2
            elif op == 4:
                self.outputs.append(get(1))
                self.pc += 2
            elif op == 5:
                self.pc = get(2) if get(1) != 0 else self.pc + 3
            elif op == 6:
                self.pc = get(2) if get(1) == 0 else self.pc + 3
            elif op == 7:
                setp(3, 1 if get(1) < get(2) else 0)
                self.pc += 4
            elif op == 8:
                setp(3, 1 if get(1) == get(2) else 0)
                self.pc += 4
            elif op == 9:
                self.rel += get(1)
                self.pc += 2
            elif op == 99:
                self.halted = True
                return self.outputs
            else:
                raise ValueError(f"bad opcode {op} at {self.pc}")
        return self.outputs


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        program = [int(x) for x in f.read().strip().split(',')]

    program[0] = 2  # insert quarters
    vm = Intcode(program, [])

    score = 0
    ball_x = 0
    paddle_x = 0
    joy = 0

    while not vm.halted:
        n0 = len(vm.outputs)
        vm.run([joy])
        new = vm.outputs[n0:]
        for i in range(0, len(new), 3):
            x, y, tid = new[i], new[i + 1], new[i + 2]
            if x == -1 and y == 0:
                score = tid
            elif tid == 4:
                ball_x = x
            elif tid == 3:
                paddle_x = x
        if ball_x > paddle_x:
            joy = 1
        elif ball_x < paddle_x:
            joy = -1
        else:
            joy = 0

    print(score)


if __name__ == "__main__":
    main()
