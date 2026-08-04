import os
import sys


def parse(data, pos):
    version = int(data[pos:pos + 3], 2)
    pos += 3
    type_id = int(data[pos:pos + 3], 2)
    pos += 3
    if type_id == 4:
        value = 0
        while True:
            group = data[pos:pos + 5]
            pos += 5
            value = (value << 4) | int(group[1:], 2)
            if group[0] == '0':
                break
        return pos, value
    values = []
    length_type = data[pos]
    pos += 1
    if length_type == '0':
        length = int(data[pos:pos + 15], 2)
        pos += 15
        end = pos + length
        while pos < end:
            pos, val = parse(data, pos)
            values.append(val)
    else:
        count = int(data[pos:pos + 11], 2)
        pos += 11
        for _ in range(count):
            pos, val = parse(data, pos)
            values.append(val)
    if type_id == 0:
        value = sum(values)
    elif type_id == 1:
        value = 1
        for v in values:
            value *= v
    elif type_id == 2:
        value = min(values)
    elif type_id == 3:
        value = max(values)
    elif type_id == 5:
        value = 1 if values[0] > values[1] else 0
    elif type_id == 6:
        value = 1 if values[0] < values[1] else 0
    elif type_id == 7:
        value = 1 if values[0] == values[1] else 0
    return pos, value


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        hex_data = f.read().strip()

    data = bin(int(hex_data, 16))[2:].zfill(len(hex_data) * 4)
    _, value = parse(data, 0)
    print(value)


if __name__ == "__main__":
    main()
