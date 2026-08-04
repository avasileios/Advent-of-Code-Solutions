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

    # topmost non-transparent pixel
    image = []
    for i in range(size):
        for layer in layers:
            if layer[i] != '2':
                image.append(layer[i])
                break
        else:
            image.append('2')

    # print the 6 lines of the message (0 = black, 1 = white)
    for y in range(H):
        row = ''.join('#' if image[y * W + x] == '1' else ' '
                      for x in range(W))
        print(row)


if __name__ == "__main__":
    main()
