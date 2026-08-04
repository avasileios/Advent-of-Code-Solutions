import os
import sys
from collections import deque, defaultdict
from math import lcm


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    mods = {}
    for line in lines:
        name, dests = line.split(' -> ')
        if name == 'broadcaster':
            mods['broadcaster'] = ('B', dests.split(', '))
        else:
            t = name[0]
            mods[name[1:]] = (t, dests.split(', '))

    ff = {name: False for name, (t, _) in mods.items() if t == '%'}
    conj = {name: {} for name, (t, _) in mods.items() if t == '&'}
    for name, (t, dests) in mods.items():
        for d in dests:
            if d in conj:
                conj[d][name] = False

    # find the module feeding 'rx'
    rx_src = None
    for name, (t, dests) in mods.items():
        if 'rx' in dests:
            rx_src = name
    # rx_src is a conjunction; find its inputs
    rx_inputs = [name for name, (t, dests) in mods.items() if rx_src in dests]
    seen = {}
    periods = {}

    presses = 0
    while len(periods) < len(rx_inputs):
        presses += 1
        q = deque([('button', 'broadcaster', False)])
        while q:
            src, tgt, pulse = q.popleft()
            if tgt == rx_src and pulse:
                if src not in seen:
                    seen[src] = presses
                elif src not in periods:
                    periods[src] = presses - seen[src]
            if tgt not in mods:
                continue
            t, dests = mods[tgt]
            if t == 'B':
                for d in dests:
                    q.append((tgt, d, pulse))
            elif t == '%':
                if not pulse:
                    ff[tgt] = not ff[tgt]
                    for d in dests:
                        q.append((tgt, d, ff[tgt]))
            else:
                conj[tgt][src] = pulse
                out = not all(conj[tgt].values())
                for d in dests:
                    q.append((tgt, d, out))

    result = 1
    for p in periods.values():
        result = lcm(result, p)
    print(result)


if __name__ == "__main__":
    main()
