import os
import sys
import re


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


DANGEROUS = {"infinite loop", "giant electromagnet", "escape pod",
             "photons", "molten lava"}

OPPOSITE = {"north": "south", "south": "north",
            "east": "west", "west": "east"}


def parse_room(text):
    name_m = re.search(r'== (.+?) ==', text)
    name = name_m.group(1) if name_m else '?'
    items = []
    exits = []
    in_items = False
    for line in text.splitlines():
        if line.startswith('Items here:'):
            in_items = True
        elif line.startswith('Doors here lead:'):
            in_items = False
        elif line.startswith('- '):
            if in_items:
                items.append(line[2:])
            else:
                exits.append(line[2:])
    return name, items, exits


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        program = [int(x) for x in f.read().strip().split(',')]

    vm = Intcode(program, [])
    idx = 0

    def read_all():
        nonlocal idx
        new = vm.outputs[idx:]
        idx = len(vm.outputs)
        return ''.join(chr(c) for c in new if 0 < c < 128)

    def send(cmd):
        vm.run([ord(c) for c in cmd + '\n'])
        return read_all()

    text = read_all()
    if not text:
        vm.run([])
        text = read_all()

    inventory = []
    checkpoint = None
    pressure_door = None
    checkpoint_route = []

    # DFS exploration of every room, skipping the pressure floor
    visited = set()
    path = []
    while True:
        name, items, exits = parse_room(text)
        if name == 'Pressure-Sensitive Floor':
            # we're back on the floor: leave
            text = send(OPPOSITE[pressure_door] if pressure_door else 'north')
            continue
        if name == 'Security Checkpoint' and checkpoint is None:
            checkpoint = text
        if name == '?':
            # a failed move: go back where we came from
            if path:
                _, back = path.pop()
                text = send(back)
            else:
                break
            continue
        for item in items:
            if item not in DANGEROUS and item not in inventory:
                send(f"take {item}")
                inventory.append(item)
        moved = False
        for ex in exits:
            nxt = send(ex)
            nname = parse_room(nxt)[0]
            if nname == 'Pressure-Sensitive Floor':
                pressure_door = ex
                send(OPPOSITE[ex])
                continue
            if nname not in visited:
                visited.add(nname)
                path.append((name, OPPOSITE[ex]))
                if checkpoint is None:
                    checkpoint_route.append(ex)
                text = nxt
                moved = True
                break
            send(OPPOSITE[ex])
        if moved:
            continue
        if not path:
            break
        _, back = path.pop()
        text = send(back)
        if checkpoint is None and checkpoint_route:
            checkpoint_route.pop()

    if pressure_door is None:
        # find the pressure floor door from the checkpoint
        name, items, exits = parse_room(checkpoint)
        for ex in exits:
            nxt = send(ex)
            if parse_room(nxt)[0] == 'Pressure-Sensitive Floor':
                pressure_door = ex
                send(OPPOSITE[ex])
                break

    # get back to the checkpoint
    while path:
        _, back = path.pop()
        text = send(back)
    for cmd in checkpoint_route:
        text = send(cmd)

    # brute-force the item subset on the pressure floor.  All items are on
    # the checkpoint floor (dropped there); after an ejection the robot is
    # automatically back at the checkpoint.
    held = set()
    for mask in range(1 << len(inventory)):
        subset = {inventory[i] for i in range(len(inventory))
                  if mask & (1 << i)}
        for item in held - subset:
            send(f"drop {item}")
        for item in subset - held:
            send(f"take {item}")
        held = subset
        r = send(pressure_door)
        if "ejected" in r or "heavier" in r or "lighter" in r or \
                "wrong" in r:
            continue
        # success: extract the code (may be a number, e.g. "229384")
        codes = re.findall(r'"([A-Za-z0-9]+)"', r)
        if codes:
            print(codes[-1])
        else:
            print(r[-800:])
        return


if __name__ == "__main__":
    main()
