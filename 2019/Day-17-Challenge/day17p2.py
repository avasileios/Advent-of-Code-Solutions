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


def compress(tokens):
    """Compress a flat token list (e.g. ['R','6','L','8',...]) into a main
    routine and up to three functions, each <= 20 chars when joined."""
    names = "ABC"
    solution = [None]

    def search(i, pats, main, used):
        if solution[0]:
            return True
        if i >= len(tokens):
            if len(pats) == 3 and all(used) and len(','.join(main)) <= 20:
                solution[0] = (main[:], pats[:])
                return True
            return False
        if len(','.join(main)) > 20:
            return False
        for pi, (name, p) in enumerate(pats):
            if tokens[i:i + len(p)] == p:
                used[pi] = True
                main.append(name)
                if search(i + len(p), pats, main, used):
                    return True
                main.pop()
                used[pi] = False
        if len(pats) < 3:
            for L in range(1, len(tokens) - i + 1):
                p = tokens[i:i + L]
                if len(','.join(p)) > 20:
                    break
                main.append(names[len(pats)])
                if search(i + L, pats + [(names[len(pats)], p)],
                          main, used + [True]):
                    return True
                main.pop()
        return False

    search(0, [], [], [])
    return solution[0]


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        program = [int(x) for x in f.read().strip().split(',')]

    vm = Intcode(program, [])
    out = vm.run()
    text = ''.join(chr(c) for c in out)
    grid = [list(line) for line in text.splitlines() if line]

    h = len(grid)
    w = len(grid[0])
    dirs = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
    robot = None
    d = None
    for y in range(h):
        for x in range(w):
            if grid[y][x] in dirs:
                robot = (x, y)
                d = dirs[grid[y][x]]

    def on_scaffold(p):
        x, y = p
        return 0 <= x < w and 0 <= y < h and grid[y][x] == '#'

    def turn_left(v):
        return (v[1], -v[0])

    def turn_right(v):
        return (-v[1], v[0])

    # walk the scaffold, recording (turn, distance) pairs
    moves = []
    pos = robot
    while True:
        left = turn_left(d)
        right = turn_right(d)
        if on_scaffold((pos[0] + left[0], pos[1] + left[1])):
            turn = 'L'
            d = left
        elif on_scaffold((pos[0] + right[0], pos[1] + right[1])):
            turn = 'R'
            d = right
        else:
            break
        steps = 0
        while on_scaffold((pos[0] + d[0], pos[1] + d[1])):
            pos = (pos[0] + d[0], pos[1] + d[1])
            steps += 1
        moves.append((turn, steps))

    # flat tokens: 'R','6','L','8',... (the program expects the commas)
    tokens = []
    for turn, dist in moves:
        tokens.append(turn)
        tokens.append(str(dist))

    main_routine, patterns = compress(tokens)
    main_str = ','.join(main_routine)
    funcs = [','.join(p) for _, p in patterns]

    # run the vacuum robot
    program[0] = 2
    vm = Intcode(program, [])
    feed = '\n'.join([main_str] + funcs + ['n\n'])
    vm.run([ord(c) for c in feed])
    # the last non-ASCII output is the answer
    answer = [c for c in vm.outputs if c > 127]
    print(answer[-1])


if __name__ == "__main__":
    main()
