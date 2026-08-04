import os
import sys


def hash_str(s):
    v = 0
    for c in s:
        v = ((v + ord(c)) * 17) % 256
    return v


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read().strip()

    boxes = [{} for _ in range(256)]  # label -> focal (dict preserves order)
    for part in data.split(','):
        if '=' in part:
            label, focal = part.split('=')
            boxes[hash_str(label)][label] = int(focal)
        else:
            label = part[:-1]
            boxes[hash_str(label)].pop(label, None)

    total = 0
    for bi, box in enumerate(boxes, 1):
        for si, (label, focal) in enumerate(box.items(), 1):
            total += bi * si * focal
    print(total)


if __name__ == "__main__":
    main()
