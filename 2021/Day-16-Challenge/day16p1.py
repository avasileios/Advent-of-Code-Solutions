import os
import sys


def parse(data, pos):
    version = int(data[pos:pos + 3], 2)
    pos += 3
    type_id = int(data[pos:pos + 3], 2)
    pos += 3
    if type_id == 4:  # literal
        value = 0
        while True:
            group = data[pos:pos + 5]
            pos += 5
            value = (value << 4) | int(group[1:], 2)
            if group[0] == '0':
                break
        return version, pos, value
    # operator
    values = []
    length_type = data[pos]
    pos += 1
    if length_type == '0':
        length = int(data[pos:pos + 15], 2)
        pos += 15
        end = pos + length
        while pos < end:
            v, pos, val = parse(data, pos)
            version += v
            values.append(val)
    else:
        count = int(data[pos:pos + 11], 2)
        pos += 11
        for _ in range(count):
            v, pos, val = parse(data, pos)
            version += v
            values.append(val)
    return version, pos, values


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        hex_data = f.read().strip()

    data = bin(int(hex_data, 16))[2:].zfill(len(hex_data) * 4)
    version, _, _ = parse(data, 0)
    print(version)


if __name__ == "__main__":
    main()
