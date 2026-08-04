import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read().strip()

    W, H = 25, 6
    size = W * H
    layers = [data[i:i + size] for i in range(0, len(data), size)]

    best = None
    result = 0
    for layer in layers:
        zeros = layer.count('0')
        if best is None or zeros < best:
            best = zeros
            result = layer.count('1') * layer.count('2')

    print(result)


if __name__ == "__main__":
    main()
