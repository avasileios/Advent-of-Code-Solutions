import os
import sys
from collections import deque


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

    vm = Intcode(program, [])
    moves = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
    reverse = {1: 2, 2: 1, 3: 4, 4: 3}

    def probe(d):
        n0 = len(vm.outputs)
        vm.run([d])
        return vm.outputs[n0:][-1] if vm.outputs[n0:] else 0

    grid = {(0, 0): '.'}
    oxygen = None
    pos = (0, 0)
    tried = {(0, 0): set()}
    path = []

    while True:
        options = [d for d in (1, 2, 3, 4) if d not in tried[pos]]
        if options:
            d = options[0]
            tried[pos].add(d)
            dx, dy = moves[d]
            target = (pos[0] + dx, pos[1] + dy)
            status = probe(d)
            if status == 0:
                grid[target] = '#'
            else:
                grid[target] = 'O' if status == 2 else '.'
                if status == 2:
                    oxygen = target
                path.append((pos, d))
                pos = target
                tried.setdefault(pos, set())
        else:
            if not path:
                break
            prev, d = path.pop()
            probe(reverse[d])
            pos = prev

    # BFS from the oxygen system: how long until the whole area fills
    dist = {oxygen: 0}
    q = deque([oxygen])
    max_dist = 0
    while q:
        cur = q.popleft()
        max_dist = max(max_dist, dist[cur])
        for dx, dy in moves.values():
            nxt = (cur[0] + dx, cur[1] + dy)
            if grid.get(nxt) in ('.', 'O') and nxt not in dist:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)

    print(max_dist)


if __name__ == "__main__":
    main()
