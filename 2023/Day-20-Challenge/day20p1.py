import os
import sys
from collections import deque, defaultdict


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

    # init flip-flop states (off) and conjunction memory
    ff = {name: False for name, (t, _) in mods.items() if t == '%'}
    conj = {name: {} for name, (t, _) in mods.items() if t == '&'}
    # wire up conjunction inputs
    for name, (t, dests) in mods.items():
        for d in dests:
            if d in conj:
                conj[d][name] = False

    low = high = 0
    for _ in range(1000):
        # (source, target, pulse)
        q = deque([('button', 'broadcaster', False)])
        while q:
            src, tgt, pulse = q.popleft()
            if pulse:
                high += 1
            else:
                low += 1
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
            else:  # &
                conj[tgt][src] = pulse
                out = not all(conj[tgt].values())
                for d in dests:
                    q.append((tgt, d, out))

    print(low * high)


if __name__ == "__main__":
    main()
