import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    seeds = list(map(int, lines[0].split(': ')[1].split()))
    maps = []
    current = []
    for line in lines[2:]:
        if 'map' in line:
            if current:
                maps.append(current)
            current = []
        else:
            current.append(tuple(map(int, line.split())))
    maps.append(current)

    def apply(seed):
        v = seed
        for m in maps:
            for dst, src, rng in m:
                if src <= v < src + rng:
                    v = dst + (v - src)
                    break
        return v

    print(min(apply(s) for s in seeds))


if __name__ == "__main__":
    main()
