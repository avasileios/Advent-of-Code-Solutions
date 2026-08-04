import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.rstrip('\n') for l in f]

    sizes = {}
    stack = []
    for line in lines:
        if line.startswith('$ cd '):
            d = line[5:]
            if d == '/':
                stack = ['/']
            elif d == '..':
                stack.pop()
            else:
                stack.append(d)
        elif line.startswith('$ ls') or line.startswith('dir'):
            continue
        else:
            size, _ = line.split()
            for i in range(len(stack)):
                key = '/' + '/'.join(stack[1:i + 1])
                sizes[key] = sizes.get(key, 0) + int(size)

    total_used = sizes['/']
    free = 70000000 - total_used
    need = 30000000 - free
    candidates = [v for v in sizes.values() if v >= need]
    print(min(candidates))


if __name__ == "__main__":
    main()
