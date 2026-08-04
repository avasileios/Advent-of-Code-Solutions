import os
import sys
import re


def mask_addresses(addr, mask):
    """Yield all addresses after applying the floating mask."""
    addrs = [0]
    for i, c in enumerate(mask):
        bit = 35 - i
        if c == '0':
            # keep the address's bit
            addrs = [a | (addr & (1 << bit)) for a in addrs]
        elif c == '1':
            addrs = [a | (1 << bit) for a in addrs]
        else:  # 'X': floating
            new = []
            for a in addrs:
                new.append(a & ~(1 << bit))       # bit 0
                new.append(a | (1 << bit))        # bit 1
            addrs = new
    return addrs


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    mem = {}
    mask = 'X' * 36
    for line in lines:
        if line.startswith('mask'):
            mask = line.split(' = ')[1]
        else:
            m = re.match(r'mem\[(\d+)\] = (\d+)', line)
            addr, value = int(m.group(1)), int(m.group(2))
            for a in mask_addresses(addr, mask):
                mem[a] = value

    print(sum(mem.values()))


if __name__ == "__main__":
    main()
